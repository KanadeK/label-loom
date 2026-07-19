from pathlib import Path

from label_loom.cli import main


def test_cli_generates_csv_and_round_log(tmp_path: Path) -> None:
    input_path = Path("examples/demo_pool.csv")
    output, ledger = tmp_path / "recommendations.csv", tmp_path / "rounds.json"
    exit_code = main(
        [
            "recommend",
            str(input_path),
            "--output",
            str(output),
            "--ledger",
            str(ledger),
            "--strategy",
            "diversity",
            "--budget",
            "4",
            "--batch-size",
            "4",
        ]
    )
    assert exit_code == 0
    assert output.read_text(encoding="utf-8").count("\n") == 5
    assert ledger.exists()
