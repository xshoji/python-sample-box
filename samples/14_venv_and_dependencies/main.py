"""仮想環境（venv）と依存パッケージの隔離を、実行時の環境情報で確認するサンプル。

このスクリプトは 3rd party ライブラリには一切依存しません。
代わりに、いま動いている Python が

- どこにある実行ファイルか
- system Python なのか、venv の Python なのか
- site-packages（外部パッケージの置き場）はどこか

を表示し、venv の有効化前後で何が変わるかを目で確認できるようにしています。

詳しい使い方・背景は同ディレクトリの README.md を参照。
"""

from __future__ import annotations

import site
import sys
from pathlib import Path


def in_virtualenv() -> bool:
    """現在の Python が venv（または virtualenv）配下で動いているか判定する。

    venv で作られた Python では ``sys.prefix`` が venv のディレクトリを指し、
    ``sys.base_prefix`` が元の system Python を指す。両者が違えば venv の中。
    """
    return sys.prefix != sys.base_prefix


def main() -> None:
    print("# interpreter location")
    print(f"sys.executable   : {sys.executable}")
    print(f"sys.prefix       : {sys.prefix}")
    print(f"sys.base_prefix  : {sys.base_prefix}")

    print("\n# venv?")
    if in_virtualenv():
        venv_root = Path(sys.prefix)
        print(f"running inside a virtual environment: {venv_root}")
    else:
        print("running on the *system* / non-venv Python")
        print("→ pip install するとこの Python 全体に影響します")

    print("\n# where would `pip install <pkg>` put files?")
    # ユーザー環境によっては複数ある（system + user site）。venv 内ではほぼ 1 つに集約される。
    for path in site.getsitepackages():
        print(f"site-packages    : {path}")
    try:
        print(f"user site        : {site.getusersitepackages()}")
    except Exception as exc:  # pragma: no cover - 環境依存の保険
        print(f"user site        : (unavailable: {exc})")


if __name__ == "__main__":
    main()
