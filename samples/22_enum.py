"""`enum` モジュール: Python の列挙型。

Python の Enum は単なる定数群ではなく、**メソッドを持てる完全なクラス** です。
Java の enum に近い（値ごとの振る舞い、メソッド定義、iter 可能）。

扱うもの:

- `Enum`           : 値の意味だけを区別したいときの基本形
- `IntEnum`        : 値が int として振る舞う（int との比較が成り立つ）
- `StrEnum` (3.11+): 値が str として振る舞う（API レスポンスや JSON で便利）
- `auto()`         : 値を自動採番させる
- メソッド定義     : enum 自体にロジックを持たせる
"""

from enum import Enum, IntEnum, StrEnum, auto


# ============================================================
# 基本: Enum
# ============================================================
# - 各メンバーは「クラスのインスタンス」。Color.RED is Color.RED が True
# - `Color.RED == 1` のような int との比較は False（型が違う）
# - 列挙の順序は定義順
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    def to_hex(self) -> str:
        # enum にメソッドを定義できる。Java の enum と同じ感覚。
        return {
            Color.RED: "#ff0000",
            Color.GREEN: "#00ff00",
            Color.BLUE: "#0000ff",
        }[self]


# ============================================================
# IntEnum: int として振る舞う
# ============================================================
# 既存の int を使う API（HTTP ステータスコードなど）と互換性を保ちたい場合に便利。
# Status.OK == 200 が True になる。
class Status(IntEnum):
    OK = 200
    NOT_FOUND = 404
    SERVER_ERROR = 500


# ============================================================
# StrEnum (3.11+): str として振る舞う
# ============================================================
# JSON / 設定ファイル / API レスポンスで「文字列として渡す列挙値」によく使う。
# Role.ADMIN == "admin" が True になる。
class Role(StrEnum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


# ============================================================
# auto(): 値を自動採番させる
# ============================================================
# 値そのものに意味が無い場合、auto() に任せると保守が楽。
# Enum では 1, 2, 3... が振られる。StrEnum では小文字のメンバー名が振られる。
class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


def main() -> None:
    print("--- Enum 基本 ---")
    print(f"  Color.RED        = {Color.RED!r}")
    print(f"  Color.RED.name   = {Color.RED.name}")
    print(f"  Color.RED.value  = {Color.RED.value}")
    print(f"  Color.RED.to_hex = {Color.RED.to_hex()}")
    print(f"  Color.RED is Color.RED  -> {Color.RED is Color.RED}")
    print(f"  Color.RED == 1          -> {Color.RED == 1}  # 普通の Enum は int と非互換")

    print("\n--- iteration ---")
    # for で列挙すると定義順に全メンバーが取れる
    for c in Color:
        print(f"  {c.name} -> value={c.value}, hex={c.to_hex()}")

    print("\n--- IntEnum: int として振る舞う ---")
    print(f"  Status.OK            = {Status.OK!r}")
    print(f"  Status.OK == 200     -> {Status.OK == 200}")
    print(f"  Status.OK + 1        -> {Status.OK + 1}  # int 演算もできる")

    print("\n--- StrEnum (3.11+): str として振る舞う ---")
    print(f"  Role.ADMIN           = {Role.ADMIN!r}")
    print(f"  Role.ADMIN == 'admin' -> {Role.ADMIN == 'admin'}")
    print(f"  f'role={{Role.ADMIN}}' -> 'role={Role.ADMIN}'  # そのまま文字列補間できる")

    print("\n--- auto() ---")
    for d in Direction:
        print(f"  {d.name} -> value={d.value}")

    print("\n--- 値からメンバーを取る ---")
    # Color(value) でメンバーを取れる。存在しない値だと ValueError。
    print(f"  Color(2)       -> {Color(2)}")
    print(f"  Status(404)    -> {Status(404)}")
    print(f"  Role('editor') -> {Role('editor')}")


if __name__ == "__main__":
    main()
