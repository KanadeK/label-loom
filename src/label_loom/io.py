"""CSV input and reproducible export adapters."""

from __future__ import annotations

import json
from pathlib import Path

import polars as pl

from label_loom.domain import Recommendation, Record


def load_csv(path: Path, text_column: str = "text", label_column: str = "label") -> list[Record]:
    if not path.is_file():
        raise FileNotFoundError(f"input file does not exist: {path}")
    frame = pl.read_csv(path, null_values=[""])
    if text_column not in frame.columns:
        raise ValueError(f"CSV must contain a '{text_column}' column")
    return [
        Record(
            id=str(row.get("id") or index),
            text=str(row[text_column]),
            label=None if row.get(label_column) is None else str(row.get(label_column)),
        )
        for index, row in enumerate(frame.iter_rows(named=True), start=1)
    ]


def export_recommendations(items: list[Recommendation], target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = [item.__dict__ for item in items]
    if target.suffix.lower() == ".json":
        target.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return
    if target.suffix.lower() != ".csv":
        raise ValueError("export target must end in .csv or .json")
    pl.DataFrame(
        rows, schema=["id", "text", "predicted_label", "uncertainty", "diversity", "score"]
    ).write_csv(target)
