from pathlib import Path

import numpy as np
import polars as pl
from sklearn.metrics import f1_score

from label_loom.domain import Record, SelectionConfig, TextActiveLearner


def test_hybrid_learning_curve_beats_fixed_random_baseline() -> None:
    """The bundled fixed-seed scenario is a regression guard for selection quality."""
    rows = list(pl.read_csv(Path("examples/demo_pool.csv"), null_values=[""]).iter_rows(named=True))
    records = [Record(id=str(row["id"]), text=str(row["text"]), label=row["label"]) for row in rows]
    truth = {str(row["id"]): str(row["ground_truth"]) for row in rows}
    initial = [record for record in records if record.label is not None]
    pool = [record for record in records if record.label is None]

    learner = TextActiveLearner(seed=42)
    learner.fit(initial)
    hybrid_ids = {
        item.id
        for item in learner.recommend(
            records, SelectionConfig("hybrid", budget=6, batch_size=6, seed=42)
        )
    }
    random_indices = np.random.default_rng(1).choice(len(pool), size=6, replace=False)
    random_ids = {pool[int(index)].id for index in random_indices}

    def macro_f1(newly_labeled: set[str]) -> float:
        labeled = initial + [
            Record(id=record.id, text=record.text, label=truth[record.id])
            for record in pool
            if record.id in newly_labeled
        ]
        evaluation = [record for record in pool if record.id not in newly_labeled]
        model = TextActiveLearner(seed=42)
        model.fit(labeled)
        predicted = model.model.predict(
            model.vectorizer.transform([record.text for record in evaluation])
        )
        return float(
            f1_score([truth[record.id] for record in evaluation], predicted, average="macro")
        )

    assert macro_f1(hybrid_ids) >= macro_f1(random_ids) + 0.02
