"""import 名から標準ライブラリ / 3rd party / 自前コードを見分けるヒント。

Python の import 文は `import json` も `import requests` も同じ形なので、
Java の `java.*` や Go の `github.com/...` ほど見た目だけでは判別しにくい。
実務では `sys.stdlib_module_names`、`importlib.util.find_spec()`、依存定義、import の並び順で判断する。
"""

import importlib.util
import sys
from pathlib import Path


def describe_import(name: str) -> str:
    top_level_name = name.split(".")[0]
    is_stdlib = top_level_name in sys.stdlib_module_names
    spec = importlib.util.find_spec(top_level_name)

    if spec is None:
        origin = "見つからない（未インストール、または現在の sys.path から見えない）"
    else:
        origin = spec.origin or "namespace package などで origin が無い"

    if is_stdlib:
        category = "標準ライブラリ候補"
    elif spec is None:
        category = "3rd party または自前コードかもしれないが、今の環境では import 不可"
    elif "site-packages" in origin or "dist-packages" in origin:
        category = "3rd party 候補"
    else:
        category = "自前コード / 実行環境由来の module 候補"

    return f"{name:12} | {category} | {origin}"


def main() -> None:
    print("--- 1. import 文だけでは確実に判別できない ---")
    print("import json      # 標準ライブラリ")
    print("import requests  # 3rd party の代表例。ただし未インストールなら import できない")
    print("import my_app    # 自分のプロジェクトかもしれない")

    print("\n--- 2. Python 3.10+ なら sys.stdlib_module_names で標準ライブラリ名を確認できる ---")
    for name in ["json", "pathlib", "sqlite3", "requests"]:
        top_level_name = name.split(".")[0]
        print(f"{name:8} -> {top_level_name in sys.stdlib_module_names}")

    print("\n--- 3. importlib.util.find_spec() で実体の場所を見る ---")
    for name in ["sys", "json", "pathlib", "sqlite3", "requests", "pydantic", "my_app"]:
        print(describe_import(name))

    print("\n--- 4. import の並び順もヒントになる ---")
    print(
        """
# 1. 標準ライブラリ
import json
import sys
from pathlib import Path

# 2. 3rd party
import requests
from pydantic import BaseModel

# 3. 自前コード
from my_app.models import User
""".strip()
    )

    print("\n--- 5. 注意: ローカルファイル名と標準ライブラリ名の衝突 ---")
    print(f"このファイル名: {Path(__file__).name}")
    print(
        """
Python は import 対象を sys.path に並んだ場所から順に探す。
そのため、プロジェクト内に標準ライブラリと同名のファイルを作ると事故りやすい。

例:
project/
  json.py      # 自前ファイル
  main.py

main.py で `import json` したとき、標準ライブラリの json ではなく、
プロジェクト内の json.py が先に見つかる可能性がある。

避けたい名前の例:
  json.py, logging.py, pathlib.py, typing.py, email.py, sqlite3.py, re.py

対策:
  - 自前ファイルに標準ライブラリ名を付けない
  - import が怪しいときは importlib.util.find_spec("json").origin で実体の場所を見る
""".strip()
    )


if __name__ == "__main__":
    main()
