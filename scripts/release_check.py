"""Check release prerequisites using real repository state and quality gates."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = re.compile(
    r"TODO|FIXME|NotImplemented|placeholder|coming soon|lorem ipsum", re.IGNORECASE
)
SECRET_ASSIGNMENT = re.compile(
    r"(?:api[_-]?key|secret|token|password)\s*=\s*[\"'][^\"']+", re.IGNORECASE
)


def output(command: list[str]) -> str:
    return subprocess.check_output(command, cwd=ROOT, text=True).strip()


def main() -> int:
    if output(["git", "status", "--porcelain"]):
        raise SystemExit("release check requires a clean worktree")
    if "## [0.1.0]" not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"):
        raise SystemExit("CHANGELOG.md is missing v0.1.0")
    if 'version = "0.1.0"' not in (ROOT / "pyproject.toml").read_text(encoding="utf-8"):
        raise SystemExit("project metadata version is not 0.1.0")
    if not list((ROOT / "dist-release").glob("*.whl")):
        raise SystemExit("dist-release is missing wheel artifacts")
    source_text = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "src").rglob("*.py")
    )
    if FORBIDDEN.search(source_text):
        raise SystemExit("source contains an incomplete-work marker")
    tracked_files = output(["git", "ls-files"]).splitlines()
    tracked_text = "\n".join((ROOT / file).read_text(encoding="utf-8") for file in tracked_files)
    if SECRET_ASSIGNMENT.search(tracked_text):
        raise SystemExit("tracked files appear to contain a credential assignment")
    author = output(["git", "log", "-1", "--format=%an <%ae> | %cn <%ce>"])
    if "KanadeK" not in author:
        raise SystemExit("latest commit author does not match the logged-in account")
    subprocess.run([sys.executable, "scripts/verify.py"], cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
