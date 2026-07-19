"""Render the bundled CLI result as a committed, reproducible SVG preview."""

from __future__ import annotations

import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    source = ROOT / "examples" / "demo_recommendations.csv"
    rows = list(csv.DictReader(source.open(encoding="utf-8")))
    lines = ["Label Loom • hybrid recommendation batch"]
    lines.extend(f"{row['id']}  {row['predicted_label']:<10} score {row['score']}" for row in rows)
    text = "".join(
        (
            f'<text x="32" y="{68 + index * 30}" font-family="monospace" '
            f'font-size="16" fill="#e2e8f0">{escape(line)}</text>'
        )
        for index, line in enumerate(lines)
    )
    height = 100 + 30 * len(lines)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{height}" '
        f'viewBox="0 0 760 {height}"><rect width="100%" height="100%" fill="#0f172a" '
        f'rx="16"/>{text}</svg>\n'
    )
    (ROOT / "docs" / "demo-output.svg").write_text(svg, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
