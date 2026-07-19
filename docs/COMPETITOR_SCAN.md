# Public repository sample scan

Checked 2026-07-19 using the authenticated GitHub CLI. Exact searches for `"Label Loom"` returned no results; `label-loom` returned only unrelated label-design/front-end repositories. The target slug was available at the time of the scan.

| Repository | Stars | Updated | Main scope | Relation to Label Loom |
|---|---:|---|---|---|
| [modAL](https://github.com/modAL-python/modAL) | 2357 | 2026-07-10 | Modular Python active-learning framework | Broader framework; no focused local annotation ledger workflow |
| [adaptive](https://github.com/python-adaptive/adaptive) | 1222 | 2026-07-13 | Parallel mathematical-function learning | Different problem domain |
| [google/active-learning](https://github.com/google/active-learning) | 1166 | 2026-06-29 | Active-learning research code | Broader research infrastructure |
| [awesome-active-learning](https://github.com/SupeRuier/awesome-active-learning) | 995 | 2026-07-16 | Resource collection | Not an application |
| [pytorch_active_learning](https://github.com/rmunro/pytorch_active_learning) | 994 | 2026-06-23 | PyTorch human-in-the-loop library | Deep-learning library rather than local CSV workflow |
| [ASReview](https://github.com/asreview/asreview) | 948 | 2026-07-18 | Systematic-review active learning | Specialized review screening |
| [BaaL](https://github.com/baal-org/baal) | 933 | 2026-07-06 | Bayesian active-learning library | Research/industrial Bayesian framework |
| [ALiPy](https://github.com/NUAA-AL/ALiPy) | 904 | 2026-07-15 | Active-learning toolbox | Evaluation-focused toolbox |
| [ad_examples](https://github.com/shubhomoydas/ad_examples) | 874 | 2026-06-03 | Anomaly detection and feedback | Different task family |
| [deep-active-learning](https://github.com/ej0cl6/deep-active-learning) | 850 | 2026-07-15 | Deep active-learning experiments | Deep-learning experiments |

The scan led to a deliberate scope decision: Label Loom remains an offline text-classification tool with a small sklearn baseline, explicit budget and predicted-class constraint, CSV/JSON handoff, and per-round cost record. This avoids copying wider framework designs while serving small ML teams and annotation coordinators.
