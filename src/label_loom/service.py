"""Application use cases and append-only annotation round ledger."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from label_loom.domain import Recommendation, Record, SelectionConfig, TextActiveLearner


@dataclass(frozen=True)
class RoundRecord:
    strategy: str
    selected: int
    budget: int
    cost: float
    created_at: str
    export_path: str


def recommend_and_record(
    records: list[Record],
    config: SelectionConfig,
    export_path: Path,
    ledger_path: Path,
    unit_cost: float,
) -> list[Recommendation]:
    if unit_cost < 0:
        raise ValueError("unit_cost cannot be negative")
    learner = TextActiveLearner(seed=config.seed)
    learner.fit([record for record in records if record.label is not None])
    recommendations = learner.recommend(records, config)
    from label_loom.io import export_recommendations

    export_recommendations(recommendations, export_path)
    round_record = RoundRecord(
        strategy=config.strategy,
        selected=len(recommendations),
        budget=config.budget,
        cost=round(len(recommendations) * unit_cost, 2),
        created_at=datetime.now(UTC).isoformat(),
        export_path=str(export_path),
    )
    append_round(ledger_path, round_record)
    return recommendations


def append_round(path: Path, round_record: RoundRecord) -> None:
    existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    if not isinstance(existing, list):
        raise ValueError("ledger must contain a JSON list")
    path.parent.mkdir(parents=True, exist_ok=True)
    existing.append(asdict(round_record))
    path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
