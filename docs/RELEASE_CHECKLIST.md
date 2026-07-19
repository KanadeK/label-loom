# Release checklist

- [x] Version is `0.1.0` in project metadata and changelog.
- [x] License, bilingual README, security, contributing, code of conduct, architecture, privacy, sample-data, benchmark, and competitor documentation are present.
- [x] Sample data is synthetic and offline.
- [x] Verification, demo, packaging, checksum, and clean-install checks are available.
- [x] CI, security audit, Dependabot, issue forms, and pull-request template are configured.
- [ ] Run `python scripts/verify.py`, `python scripts/demo.py`, and `python scripts/package_release.py` from the release commit.
- [ ] Run `python scripts/release_check.py` with a clean worktree after packaging.
- [ ] Confirm GitHub Actions is green, then annotate and push `v0.1.0`.
- [ ] Publish release assets and verify their checksum.
