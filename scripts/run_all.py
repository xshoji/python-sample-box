"""Run all numbered sample scripts.

サンプルは次のいずれかの形式を想定する:

- ``samples/NN_name.py``           : 単一ファイル形式
- ``samples/NN_name/main.py``      : ディレクトリ形式（README.md などを伴う）
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"


def iter_entrypoints() -> list[Path]:
    entries: list[Path] = []
    for path in SAMPLES.glob("[0-9][0-9]_*"):
        if path.is_file() and path.suffix == ".py":
            entries.append(path)
        elif path.is_dir():
            main_py = path / "main.py"
            if main_py.is_file():
                entries.append(main_py)
    # NN プレフィックス順に並べる（ファイル/ディレクトリが混在しても安定）
    return sorted(entries, key=lambda p: p.parent.name if p.name == "main.py" else p.name)


def main() -> None:
    for path in iter_entrypoints():
        relative = path.relative_to(ROOT)
        print(f"\n=== {relative} ===", flush=True)
        subprocess.run([sys.executable, str(path)], check=True)


if __name__ == "__main__":
    main()
