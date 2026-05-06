"""`json` / `csv` 標準ライブラリ: 外部データを読み書きする基本。

業務では API・ログ・CSV エクスポートなどで「外から来た文字列」を扱う場面が多い。
Python 標準ライブラリだけでも、JSON と CSV の基本的な読み書きは十分できる。
"""

import csv
import json
from dataclasses import asdict, dataclass
from io import StringIO
from typing import Any

# `Any` は「型チェッカーに、この値はどんな型として扱ってもよい」と伝える型。
# Java の `Object`、Go の `any` / `interface{}` に近いが、Python では型ヒント用の印であり、
# 実行時に値を包んだり制限したりするものではない。
# 外部入力や json.dumps の default 関数のように「何が来るか分からない境界」で使うことが多い。


@dataclass
class User:
    user_id: int
    name: str
    tags: list[str]


def dataclass_default(value: Any) -> Any:
    # json.dumps は dataclass をそのままでは扱えない。
    # default に「標準では JSON 化できない型をどう変換するか」の関数を渡す。
    # json.dumps は int / str / list / dict / None などは自力で変換できるが、
    # User のような自作クラスに出会うと、この関数を呼んで JSON 化可能な値へ変換させる。
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    raise TypeError(f"JSON に変換できない型: {type(value).__name__}")


def json_example() -> None:
    user = User(user_id=1, name="alice", tags=["admin", "paid"])

    print("--- json.dumps / json.loads ---")
    # `default=dataclass_default` により、User が出てきた時だけ dataclass_default(user) が呼ばれる。
    # ここでは User -> dict に変換され、その後は json.dumps が通常通り dict / list / str / int を処理する。
    text = json.dumps(user, default=dataclass_default, ensure_ascii=False, indent=2)
    print(text)

    loaded = json.loads(text)
    print(f"読み戻した型: {type(loaded).__name__}, name={loaded['name']}")


def csv_example() -> None:
    rows = [
        {"user_id": "1", "name": "alice", "role": "admin"},
        {"user_id": "2", "name": "bob", "role": "viewer"},
    ]

    print("\n--- csv.DictWriter / csv.DictReader ---")
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["user_id", "name", "role"])
    writer.writeheader()
    writer.writerows(rows)
    print(buffer.getvalue().strip())

    buffer.seek(0)
    reader = csv.DictReader(buffer)
    for row in reader:
        # CSV はすべて文字列として読まれる。必要なら自分で int などに変換する。
        print(f"user_id={int(row['user_id'])}, name={row['name']}, role={row['role']}")


def main() -> None:
    json_example()
    csv_example()


if __name__ == "__main__":
    main()
