"""Create a human-reviewable recommendation output from bundled data."""

from __future__ import annotations

from pathlib import Path

from label_loom.cli import main

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    raise SystemExit(
        main(
            [
                "recommend",
                str(root / "examples" / "demo_pool.csv"),
                "--output",
                str(root / "examples" / "demo_recommendations.csv"),
                "--ledger",
                str(root / "examples" / "demo_rounds.json"),
                "--strategy",
                "hybrid",
                "--budget",
                "6",
                "--batch-size",
                "6",
            ]
        )
    )
