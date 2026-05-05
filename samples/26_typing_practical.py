"""`typing` 実用編: `Protocol` / `TypedDict` / `Literal` / `NewType` / `Final`。

既存サンプル `11_type_hints_are_not_runtime_checks.py` の続編。
「実行時チェックではない」ことを踏まえた上で、OSS / 業務でよく見る型注釈を扱う。

このファイルで触れるもの:

- `Protocol`  : structural typing（duck typing の型注釈版）。Java の interface とは違う
- `TypedDict` : 「特定 key を持つ dict」の型。JSON / API レスポンスで便利
- `Literal`   : 「この値しか取らない」を型レベルで表現。フラグや mode 引数に
- `NewType`   : int / str などのプリミティブ型に意味的な区別を付ける
- `Final`     : 再代入禁止（mypy / pyright が静的に検出）
- `overload`  : 引数の型で戻り値の型が変わる関数を表現

繰り返しになるが、これらは静的解析（mypy, pyright）のための情報であり、
**実行時に強制されるわけではない**。Protocol だけは `runtime_checkable` で
isinstance チェックが可能になる例外がある。
"""

from typing import Final, Literal, NewType, Protocol, TypedDict, overload, runtime_checkable


# ============================================================
# Protocol: structural typing
# ============================================================
# Java の interface と違い、「明示的に implements する」必要がない。
# 「`area()` メソッドを持つ何か」という形で要求し、
# 偶然そのメソッドを持つクラスはすべて該当する（duck typing 的）。
# Go の interface に最も近い。
@runtime_checkable
class HasArea(Protocol):
    def area(self) -> float: ...


class Square:
    # HasArea を継承していないが、area() を持つので HasArea として通る
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side * self.side


def total_area(shapes: list[HasArea]) -> float:
    return sum(s.area() for s in shapes)


# ============================================================
# TypedDict: dict の型
# ============================================================
# 「user_id: int, name: str を持つ dict」を型として宣言する。
# JSON レスポンスの形を表すのによく使う。
# dataclass との違い: TypedDict はあくまで dict なので、JSON シリアライズが楽。
class User(TypedDict):
    user_id: int
    name: str
    is_admin: bool


def greet_user(user: User) -> str:
    # mypy 等は user["user_id"] の型を int と認識してくれる
    suffix = " (admin)" if user["is_admin"] else ""
    return f"Hello, {user['name']}#{user['user_id']}{suffix}"


# ============================================================
# Literal: 値そのものを型にする
# ============================================================
# bool フラグの代わりや、文字列の mode 指定に使う。
# 静的解析が「OK / NG しか渡せない」と検出してくれる。
def fetch(method: Literal["GET", "POST", "PUT", "DELETE"]) -> str:
    return f"sending {method} request"


# ============================================================
# NewType: 意味の違う int / str を区別する
# ============================================================
# UserId と PostId はどちらも int だが、混ぜると論理バグになる。
# NewType で別型として区別すると、静的解析で「UserId に PostId を渡す」のを検出できる。
# 実行時には素の int として振る舞う（ゼロコスト）。
UserId = NewType("UserId", int)
PostId = NewType("PostId", int)


def get_user(user_id: UserId) -> str:
    return f"user-{user_id}"


# ============================================================
# Final: 再代入禁止
# ============================================================
# 定数を表す慣習。実行時に強制はされないが、mypy / pyright は再代入を検出する。
MAX_RETRIES: Final[int] = 3


# ============================================================
# overload: 引数の型で戻り値の型が変わる
# ============================================================
# @overload で「型上の宣言」を複数並べ、最後に「実装」を 1 つ書く。
# 呼び出し側のエディタ補完が「str を渡したら str が返る」ように振る舞う。
# 実行時は最後の実装だけが使われる。
@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...
def double(x: int | str) -> int | str:
    return x * 2


def main() -> None:
    print("--- Protocol (structural typing) ---")
    shapes: list[HasArea] = [Square(2), Square(3)]
    print(f"  total area = {total_area(shapes)}")
    # @runtime_checkable を付けたので isinstance チェックも可能
    print(f"  isinstance(Square(1), HasArea) -> {isinstance(Square(1), HasArea)}")

    print("\n--- TypedDict ---")
    alice: User = {"user_id": 1, "name": "alice", "is_admin": True}
    print(f"  {greet_user(alice)}")

    print("\n--- Literal ---")
    print(f"  {fetch('GET')}")
    # fetch("get")  → mypy が「Literal['GET','POST',...] 以外」と指摘する
    # 実行時に弾きたければ自前で if method not in (...) を書く必要がある

    print("\n--- NewType ---")
    uid = UserId(42)
    print(f"  get_user(UserId(42)) = {get_user(uid)}")
    print(f"  type(uid) at runtime = {type(uid).__name__}  # 実行時は素の int")

    print("\n--- Final ---")
    print(f"  MAX_RETRIES = {MAX_RETRIES}")

    print("\n--- overload ---")
    print(f"  double(3)        = {double(3)}")
    print(f"  double('ab')     = {double('ab')}")


if __name__ == "__main__":
    main()
