"""Command-line interface for the offline Label Loom workflow."""

from __future__ import annotations

import argparse
from pathlib import Path

from label_loom import __version__
from label_loom.domain import SelectionConfig
from label_loom.io import load_csv
from label_loom.service import recommend_and_record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="label-loom", description="Offline active-learning recommendations"
    )
    parser.add_argument("--version", action="version", version=__version__)
    command = parser.add_subparsers(dest="command", required=True)
    run = command.add_parser("recommend", help="recommend a batch from a CSV pool")
    run.add_argument("input", type=Path)
    run.add_argument("--output", type=Path, default=Path("recommendations.csv"))
    run.add_argument("--ledger", type=Path, default=Path("annotation-rounds.json"))
    run.add_argument("--strategy", choices=["uncertainty", "diversity", "hybrid"], default="hybrid")
    run.add_argument("--budget", type=int, default=10)
    run.add_argument("--batch-size", type=int, default=10)
    run.add_argument("--no-class-balance", action="store_true")
    run.add_argument("--unit-cost", type=float, default=0.12)
    run.add_argument("--text-column", default="text")
    run.add_argument("--label-column", default="label")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "recommend":
        records = load_csv(args.input, args.text_column, args.label_column)
        config = SelectionConfig(
            strategy=args.strategy,
            budget=args.budget,
            batch_size=args.batch_size,
            class_balance=not args.no_class_balance,
        )
        result = recommend_and_record(records, config, args.output, args.ledger, args.unit_cost)
        message = f"recommended {len(result)} unique samples using {args.strategy}"
        print(f"{message}; exported to {args.output}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
