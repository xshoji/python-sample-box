"""Run all numbered sample scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"


def main() -> None:
    for path in sorted(SAMPLES.glob("[0-9][0-9]_*.py")):
        relative = path.relative_to(ROOT)
        print(f"\n=== {relative} ===", flush=True)
        subprocess.run([sys.executable, str(path)], check=True)


if __name__ == "__main__":
    main()
