"""Pure models and active-learning selection rules."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Literal

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, Field, field_validator
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

Strategy = Literal["uncertainty", "diversity", "hybrid"]


class Record(BaseModel):
    id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    label: str | None = None

    @field_validator("label", mode="before")
    @classmethod
    def blank_label_is_missing(cls, value: object) -> object:
        return None if value is None or str(value).strip() == "" else str(value).strip()


@dataclass(frozen=True)
class SelectionConfig:
    strategy: Strategy
    budget: int
    batch_size: int
    class_balance: bool = True
    seed: int = 42

    def __post_init__(self) -> None:
        if self.budget < 1 or self.batch_size < 1:
            raise ValueError("budget and batch_size must be positive")


@dataclass(frozen=True)
class Recommendation:
    id: str
    text: str
    predicted_label: str
    uncertainty: float
    diversity: float
    score: float


def entropy(probabilities: NDArray[np.float64]) -> NDArray[np.float64]:
    """Return normalized Shannon entropy for every probability row."""
    if probabilities.ndim != 2 or probabilities.shape[1] < 2:
        raise ValueError("entropy needs probabilities for at least two classes")
    safe = np.clip(probabilities, 1e-12, 1.0)
    values = -(safe * np.log(safe)).sum(axis=1) / np.log(probabilities.shape[1])
    return np.asarray(values, dtype=np.float64)


class TextActiveLearner:
    """A deterministic TF-IDF + logistic-regression text selection engine."""

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
        self.model = LogisticRegression(max_iter=500, random_state=seed, class_weight="balanced")
        self._fitted = False

    def fit(self, labeled: list[Record]) -> None:
        labels = [record.label for record in labeled]
        if len(labeled) < 2 or any(label is None for label in labels) or len(set(labels)) < 2:
            raise ValueError("at least two labeled classes are required to train")
        matrix = self.vectorizer.fit_transform([record.text for record in labeled])
        self.model.fit(matrix, [str(label) for label in labels])
        self._fitted = True

    def recommend(self, records: list[Record], config: SelectionConfig) -> list[Recommendation]:
        if not self._fitted:
            raise RuntimeError("fit must be called before recommend")
        pool = [record for record in records if record.label is None]
        if not pool:
            return []
        count = min(config.budget, config.batch_size, len(pool))
        vectors = self.vectorizer.transform([record.text for record in pool])
        probabilities = self.model.predict_proba(vectors)
        uncertainty_scores = entropy(probabilities)
        predicted = self.model.classes_[np.argmax(probabilities, axis=1)]
        diversity_scores = self._novelty(vectors)
        scores = self._scores(config.strategy, uncertainty_scores, diversity_scores)
        chosen = self._choose(scores, diversity_scores, predicted, count, config.class_balance)
        return [
            Recommendation(
                id=pool[index].id,
                text=pool[index].text,
                predicted_label=str(predicted[index]),
                uncertainty=round(float(uncertainty_scores[index]), 6),
                diversity=round(float(diversity_scores[index]), 6),
                score=round(float(scores[index]), 6),
            )
            for index in chosen
        ]

    @staticmethod
    def _scores(
        strategy: Strategy,
        uncertainty_scores: NDArray[np.float64],
        diversity_scores: NDArray[np.float64],
    ) -> NDArray[np.float64]:
        if strategy == "uncertainty":
            return uncertainty_scores
        if strategy == "diversity":
            return diversity_scores
        return 0.65 * uncertainty_scores + 0.35 * diversity_scores

    @staticmethod
    def _novelty(vectors: csr_matrix) -> NDArray[np.float64]:
        normalized = vectors.copy()
        similarities = (normalized @ normalized.T).toarray()
        np.fill_diagonal(similarities, 0.0)
        return np.asarray(1.0 - similarities.max(axis=1), dtype=np.float64)

    @staticmethod
    def _choose(
        scores: NDArray[np.float64],
        diversity_scores: NDArray[np.float64],
        predicted: NDArray[np.str_],
        count: int,
        class_balance: bool,
    ) -> list[int]:
        order = sorted(
            range(len(scores)), key=lambda index: (-scores[index], -diversity_scores[index], index)
        )
        if not class_balance:
            return order[:count]
        quota = ceil(count / max(1, len(set(predicted.tolist()))))
        selected: list[int] = []
        per_class: dict[str, int] = {}
        for index in order:
            label = str(predicted[index])
            if per_class.get(label, 0) < quota:
                selected.append(index)
                per_class[label] = per_class.get(label, 0) + 1
            if len(selected) == count:
                return selected
        return selected
