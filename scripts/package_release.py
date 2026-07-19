"""Build, checksum, and install-test distributable artifacts in a clean directory."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
RELEASE = ROOT / "dist-release"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    subprocess.run([sys.executable, "-m", "build"], cwd=ROOT, check=True)
    RELEASE.mkdir(exist_ok=True)
    for artifact in DIST.iterdir():
        if artifact.suffix in {".whl", ".gz"}:
            shutil.copy2(artifact, RELEASE / artifact.name)
    wheel = next(RELEASE.glob("*.whl"))
    with tempfile.TemporaryDirectory() as directory:
        environment = Path(directory) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True)
        executable = environment / (
            "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
        )
        subprocess.run([str(executable), "-m", "pip", "install", str(wheel)], check=True)
        subprocess.run([str(executable), "-m", "label_loom.cli", "--version"], check=True)
    checksums = "".join(
        f"{sha256(file)}  {file.name}\n"
        for file in sorted(RELEASE.iterdir())
        if file.is_file() and file.name != "SHA256SUMS.txt"
    )
    (RELEASE / "SHA256SUMS.txt").write_text(checksums, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
