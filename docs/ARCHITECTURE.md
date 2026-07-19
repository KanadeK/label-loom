# Architecture

```text
CSV input ──> io.load_csv ──> domain.TextActiveLearner ──> CSV/JSON export
                                  │
                                  └──> service round ledger
CLI ───────────────────────────────────────────────────────┘
```

`domain.py` owns validation, entropy, model training, scoring, diversity calculation, class-balanced selection, and reproducibility. It has no command-line or file dependency. `io.py` is the CSV/JSON adapter. `service.py` orchestrates an export and writes one append-only JSON ledger entry. `cli.py` translates user arguments into this use case.

The baseline fits TF-IDF word and bigram features followed by balanced multinomial logistic regression. Uncertainty is normalized predictive entropy. Diversity is one minus a sample's highest cosine similarity to another pool sample. Hybrid weights uncertainty at 0.65 and diversity at 0.35. Stable score and row-index ordering remove random tie behavior.
