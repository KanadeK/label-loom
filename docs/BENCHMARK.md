# Benchmark

Recorded on the repository's bundled synthetic support-text pool (24 rows, 10 initially labeled, 14 unlabeled), using Python 3.14.6 on Windows and the default fixed seed 42. `python scripts/demo.py` completed in under one second and emitted a six-row hybrid recommendation CSV plus its ledger.

The regression scenario labels the selected six samples with the synthetic ground truth, retrains, and scores the remaining pool's macro F1. Hybrid reached **0.4400**, exceeding the fixed-seed random baseline's **0.4133** by **0.0267** (required margin: 0.0200). This check is enforced in `tests/e2e/test_learning_curve.py`.

This compact benchmark measures the intended MVP use case, not production-scale training. The selection engine is deterministic for a fixed source file and configuration; users should benchmark their own language, class mix, and annotation costs before operational rollout.
