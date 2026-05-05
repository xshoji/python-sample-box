"""`match` 文（structural pattern matching, 3.10+）。

`match` は単なる値の switch ではなく、**構造に対するパターンマッチ** です。
Java の `switch` より Rust / Scala の `match`、Elixir / Erlang のパターンマッチに近い。

扱うパターン:

1. リテラル / OR パターン
2. シーケンスパターン（list / tuple の分解）
3. マッピングパターン（dict の分解）
4. クラスパターン（dataclass の属性分解）
5. ガード（if 条件）
6. ワイルドカード `_` と「捕捉」`name`
"""

from dataclasses import dataclass


# ============================================================
# 1. リテラル / OR パターン
# ============================================================
def http_label(status: int) -> str:
    match status:
        case 200 | 201 | 204:
            return "success"
        case 301 | 302:
            return "redirect"
        case 400 | 401 | 403 | 404:
            return "client error"
        case 500 | 502 | 503:
            return "server error"
        case _:
            # `_` はワイルドカード。どのパターンにも一致しなかった場合の受け皿。
            return "unknown"


# ============================================================
# 2. シーケンスパターン
# ============================================================
# `case (x, 0):` のような書き方の意味を分解する。
#
#   case (パターン1, パターン2):
#
# パターンの中身は、見た目は同じでも 2 種類ある:
#
#   - リテラル（具体値）  : `0`, `"GET"`, `True` のような「その値そのもの」
#                          → match 対象の同じ位置の要素が「この値と等しいか」を確かめる
#   - 捕捉名（キャプチャ）: `x`, `y`, `rest` のような「単なる識別子」
#                          → 何にでもマッチして、その要素を **その名前の変数に束縛する**
#                          → 束縛された変数は、その case 節の中（return まで）で使える
#
# つまり `case (x, 0):` は、
#   「2 要素の sequence で、2 番目がちょうど 0 のとき」にマッチし、
#   1 番目の要素を `x` という名前で取り出す、という意味になる。
# 入力が (5, 0) なら x = 5、(7, 0) なら x = 7、として case 節の本体で使える。
#
# 注意: 捕捉名は「ローカル変数として上書きされる」。`x = 0` のような既存の値とは
# 比較されない。「特定の値と一致したい」ときはリテラルを書くか、`Color.RED` のような
# ドット付きの名前（属性アクセス）を使う必要がある（"value pattern" と呼ぶ）。
#
# `*rest` は通常の unpacking（`a, *rest = [1, 2, 3, 4]`）と同じノリで、
# 余った要素をまとめて list として捕捉する捕捉名。
def describe_point(point: tuple) -> str:
    match point:
        case ():
            # 空 tuple とだけマッチ。捕捉名なし。
            return "empty"
        case (x, 0):
            # 「2 要素 / 2 番目がちょうど 0」。1 番目を x に束縛して使う。
            return f"on x-axis at x={x}"
        case (0, y):
            # 「2 要素 / 1 番目がちょうど 0」。2 番目を y に束縛して使う。
            return f"on y-axis at y={y}"
        case (x, y):
            # 「2 要素ならどんな値でも」。両方を x, y に束縛して使う。
            # 上の 2 つに当たらなかったケース（例: (3, 4)）がここに落ちる。
            return f"at ({x}, {y})"
        case (x, y, *rest):
            # 3 要素以上。先頭 2 つを x, y、残りを list として rest に束縛。
            # 例: (1, 2, 3, 4) → x=1, y=2, rest=[3, 4]
            return f"3D+ point: head=({x}, {y}), rest={rest}"
        case _:
            # `_` はワイルドカードかつ「束縛しない」特別な名前（変数として使えない）。
            return "not a point"


# ============================================================
# 3. マッピングパターン（dict）
# ============================================================
# dict は「指定した key だけ」を見る部分マッチ。余計な key があっても OK。
def parse_event(event: dict) -> str:
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"click at ({x}, {y})"
        case {"type": "key", "key": key}:
            return f"key pressed: {key}"
        case {"type": kind}:
            return f"unknown event kind: {kind}"
        case _:
            return "invalid event"


# ============================================================
# 4. クラスパターン（dataclass などの属性分解）
# ============================================================
@dataclass
class Circle:
    radius: float


@dataclass
class Rectangle:
    width: float
    height: float


def area(shape: object) -> float:
    match shape:
        case Circle(radius=r):
            return 3.14159 * r * r
        case Rectangle(width=w, height=h):
            return w * h
        case _:
            raise ValueError(f"unsupported shape: {shape!r}")


# ============================================================
# 5. ガード（if 条件）
# ============================================================
def classify_number(n: int) -> str:
    match n:
        case 0:
            return "zero"
        case x if x < 0:
            # `case x if 条件` で「捕捉した値に追加条件」を付けられる
            return f"negative: {x}"
        case x if x % 2 == 0:
            return f"positive even: {x}"
        case x:
            return f"positive odd: {x}"


def main() -> None:
    print("--- HTTP ステータス（リテラル / OR） ---")
    for code in [200, 301, 404, 500, 999]:
        print(f"  {code} -> {http_label(code)}")

    print("\n--- シーケンスパターン ---")
    for p in [(), (5, 0), (0, 7), (3, 4), (1, 2, 3, 4)]:
        print(f"  {p} -> {describe_point(p)}")

    print("\n--- マッピングパターン ---")
    for ev in [
        {"type": "click", "x": 10, "y": 20, "button": "left"},
        {"type": "key", "key": "Enter"},
        {"type": "scroll"},
        {"foo": "bar"},
    ]:
        print(f"  {ev} -> {parse_event(ev)}")

    print("\n--- クラスパターン ---")
    print(f"  Circle(2)        -> area = {area(Circle(2))}")
    print(f"  Rectangle(3, 4)  -> area = {area(Rectangle(3, 4))}")

    print("\n--- ガード ---")
    for n in [0, -3, 4, 7]:
        print(f"  {n} -> {classify_number(n)}")


if __name__ == "__main__":
    main()
