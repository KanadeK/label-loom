import json
from pathlib import Path

import pytest

from label_loom.domain import SelectionConfig
from label_loom.io import export_recommendations, load_csv
from label_loom.service import recommend_and_record


def test_csv_round_trip_and_ledger(tmp_path: Path) -> None:
    source = tmp_path / "pool.csv"
    source.write_text(
        "id,text,label\n"
        "1,refund for subscription,billing\n2,invoice wrong,billing\n"
        "3,password reset,access\n4,login code,access\n"
        "5,bank transfer pending,\n6,card charged twice,\n",
        encoding="utf-8",
    )
    output, ledger = tmp_path / "result.json", tmp_path / "rounds.json"
    result = recommend_and_record(
        load_csv(source), SelectionConfig("hybrid", 2, 2), output, ledger, 0.5
    )
    assert len(result) == 2
    assert len(json.loads(output.read_text(encoding="utf-8"))) == 2
    assert json.loads(ledger.read_text(encoding="utf-8"))[0]["cost"] == 1.0


def test_bad_csv_and_extension_are_rejected(tmp_path: Path) -> None:
    bad = tmp_path / "bad.csv"
    bad.write_text("id,label\n1,billing\n", encoding="utf-8")
    with pytest.raises(ValueError, match="text"):
        load_csv(bad)
    with pytest.raises(ValueError, match=".csv"):
        export_recommendations([], tmp_path / "result.txt")
