from label_loom.domain import Record, SelectionConfig, TextActiveLearner, entropy


def records() -> list[Record]:
    return [
        Record(id="1", text="refund requested for duplicate payment", label="billing"),
        Record(id="2", text="invoice total is wrong", label="billing"),
        Record(id="3", text="cannot reset my password", label="access"),
        Record(id="4", text="login code does not arrive", label="access"),
        Record(id="5", text="money sent to wrong recipient"),
        Record(id="6", text="my credit card was charged twice"),
        Record(id="7", text="account sign in fails after phone change"),
        Record(id="8", text="suspicious new device logged in"),
    ]


def test_entropy_is_normalized() -> None:
    values = entropy(__import__("numpy").array([[0.5, 0.5], [0.99, 0.01]]))
    assert values[0] == 1.0
    assert 0 < values[1] < 1


def test_hybrid_selection_is_reproducible_and_unique() -> None:
    learner = TextActiveLearner(seed=8)
    learner.fit(records()[:4])
    config = SelectionConfig(strategy="hybrid", budget=3, batch_size=3, seed=8)
    first = learner.recommend(records(), config)
    second = learner.recommend(records(), config)
    assert [item.id for item in first] == [item.id for item in second]
    assert len({item.id for item in first}) == 3
    assert all(item.score >= 0 for item in first)


def test_invalid_training_data_fails() -> None:
    learner = TextActiveLearner()
    try:
        learner.fit([Record(id="1", text="only one", label="access")])
    except ValueError as error:
        assert "two labeled classes" in str(error)
    else:
        raise AssertionError("single-class training must fail")
