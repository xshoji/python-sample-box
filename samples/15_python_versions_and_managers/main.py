"""`python` / `python3` と複数バージョン共存問題を実行で確認するサンプル。

このスクリプトは 3rd party 依存ゼロで動く。実行すると、いま動いている Python が
どのコマンドから呼ばれた何者なのか、どのバージョン管理ツール経由なのかの当たりを付けられる
情報を出力する。

詳しい背景・解決策は同ディレクトリの README.md を参照。
"""

import os
import shutil
import sys
from pathlib import Path


def show_interpreter() -> None:
    """いま動いている Python そのものの情報。"""
    print("# this interpreter")
    print(f"sys.executable : {sys.executable}")
    print(f"sys.version    : {sys.version.splitlines()[0]}")
    print(f"sys.prefix     : {sys.prefix}")
    print(f"sys.base_prefix: {sys.base_prefix}")
    print(f"in venv?       : {sys.prefix != sys.base_prefix}")


def show_path_lookup(name: str) -> None:
    """シェルが `name` コマンドをどこから解決するか（PATH の最初の 1 件）。"""
    found = shutil.which(name)
    if found is None:
        print(f"  {name:<8}: (not found on PATH)")
    else:
        # symlink を辿って実体も見せる
        real = Path(found).resolve()
        print(f"  {name:<8}: {found}  →  {real}")


def show_version_manager_hints() -> None:
    """有名なバージョン管理ツールが居るかどうかのヒント。

    存在検出だけで、どれを使うべきかは決めない。"""
    print("# version manager hints (presence only)")
    for tool in ("mise", "pyenv", "uv", "asdf"):
        path = shutil.which(tool)
        if path:
            print(f"  {tool:<6}: {path}")
        else:
            print(f"  {tool:<6}: (not installed)")

    # 環境変数に痕跡が残ることが多い
    env_hits = {k: v for k, v in os.environ.items()
                if k.startswith(("PYENV", "MISE", "UV_", "ASDF"))}
    if env_hits:
        print("  env vars:")
        for k, v in sorted(env_hits.items()):
            print(f"    {k} = {v}")


def main() -> None:
    show_interpreter()

    print("\n# `python` / `python3` resolution on this PATH")
    show_path_lookup("python")
    show_path_lookup("python3")

    print()
    show_version_manager_hints()


if __name__ == "__main__":
    main()
