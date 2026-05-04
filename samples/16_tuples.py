"""tuple は「順序を持つ、変更できない、多値の入れ物」。

list と並ぶ Python の基本コンテナですが、目的が違います。
- list  : 同じ種類のものを「集めて、足したり減らしたりする」入れ物（mutable）
- tuple : 異なる意味を持つ値を「ひとかたまりの構造」として持ち回る入れ物（immutable）

他言語との対応:
- Go の複数戻り値        `return value, err`        ≒ Python の tuple 戻り
- Java の record         `record Point(int x,int y)` ≒ Python の NamedTuple / dataclass
- TypeScript の tuple 型  `[number, string]`         ≒ そのまま tuple

このファイルでは、現場でよく見る tuple の使い方を 6 パターン紹介します。
"""

from typing import NamedTuple


def divide(a: int, b: int) -> tuple[int, int]:
    """商と余りを同時に返す。Python では関数の「複数戻り値」は tuple で表現する。

    呼び出し側で `q, r = divide(10, 3)` のように unpack すれば、
    Go の `q, r := divide(10, 3)` と似た書き味になる。
    """
    return a // b, a % b
    # ↑ 実際にはカンマ区切りで「tuple を作って返している」だけ。
    #   `return (a // b, a % b)` と書いても同じ。括弧は省略できる。


class Point(NamedTuple):
    """名前付き tuple。フィールドに名前が付くので可読性が上がる。

    Java の record や TypeScript の object 型に近い使い心地。
    値の不変性が欲しく、メソッドをほとんど持たない値オブジェクトを作るときに便利。
    後発の dataclass(frozen=True) と用途は被るが、NamedTuple は
    「tuple として unpack できる」「位置でも名前でもアクセスできる」点が違う。
    """

    x: int
    y: int


def main() -> None:
    # ====================================================================
    # 1. tuple の作り方
    # ====================================================================
    # 括弧ではなく「カンマ」が tuple を作る本体。括弧は読みやすさのため。
    point = (3, 4)            # 2 要素の tuple
    single = (42,)            # 1 要素の tuple は末尾カンマ必須（(42) はただの int）
    empty: tuple = ()         # 空 tuple は () で作る
    print(f"point={point}, single={single}, empty={empty}")

    # ====================================================================
    # 2. immutable であること（list との最大の違い）
    # ====================================================================
    # tuple は中身を書き換えられない。これは「うっかり壊れない構造」を作る土台になる。
    # 試しに代入しようとすると TypeError になる:
    #   point[0] = 99   # → TypeError: 'tuple' object does not support item assignment
    #
    # 「変えたい」場合は、新しい tuple を作り直す（関数型言語のような発想）。
    moved = (point[0] + 1, point[1])
    print(f"moved={moved}  (元の point={point} はそのまま)")

    # ====================================================================
    # 3. 関数の複数戻り値 — 現場で最頻出のパターン
    # ====================================================================
    # 「2 つ以上の値を一緒に返したい」ときに dict や専用クラスを作るほどでもない、
    # という場面で tuple がそのまま使われる。組み込みの divmod() や
    # str.partition()、os.path.split() など、標準ライブラリでも多用されている。
    quotient, remainder = divide(10, 3)
    print(f"10 / 3 = {quotient} 余り {remainder}")

    # ====================================================================
    # 4. for ループでの unpack — enumerate / dict.items の定番形
    # ====================================================================
    # iterate 対象が tuple を返すので、for の変数側でそのまま unpack して受け取る。
    # これが Python の for 文を読みやすくしている代表的なイディオム。
    languages = ["python", "go", "rust"]
    for index, name in enumerate(languages, start=1):
        # enumerate は (index, value) の tuple を順に返す
        print(f"  {index}. {name}")

    scores = {"alice": 82, "bob": 59}
    for name, score in scores.items():
        # dict.items() は (key, value) の tuple を返す
        print(f"  {name} -> {score}")

    # ====================================================================
    # 5. dict のキーや set の要素にする — hashable な複合キー
    # ====================================================================
    # tuple は immutable なので「中身が同じなら必ず同じハッシュ値」を持てる。
    # そのため dict のキーや set の要素として使える。list は mutable なので使えない。
    #   distances[ ["tokyo","osaka"] ] = ...   # → TypeError: unhashable type: 'list'
    #
    # 「2 つの値の組み合わせをキーにしたい」ときに最短で書ける手段がこれ。
    distances: dict[tuple[str, str], int] = {
        ("tokyo", "osaka"): 515,
        ("tokyo", "nagoya"): 350,
    }
    print(f"tokyo-osaka = {distances[('tokyo', 'osaka')]} km")

    # 同じ理由で、訪問済みセルの管理など「座標の集合」も tuple + set で書ける。
    visited: set[tuple[int, int]] = {(0, 0), (0, 1), (1, 0)}
    print(f"(0, 1) は訪問済み? {(0, 1) in visited}")

    # ====================================================================
    # 6. NamedTuple — 「tuple のままで、フィールドに名前を付けたい」
    # ====================================================================
    # 位置アクセス（p[0]）でも名前アクセス（p.x）でも読める。
    # tuple なので unpack もできる。3rd party ライブラリや古いコードで頻出する形。
    # 値オブジェクトとして使いたいだけなら dataclass(frozen=True) でもよい
    # （samples/10_dataclasses.py 参照）。使い分けの目安:
    #   - tuple として配ったり unpack したりしたい  → NamedTuple
    #   - 普通のクラスに近い使い方をしたい           → dataclass(frozen=True)
    p = Point(x=3, y=4)
    print(f"p.x={p.x}, p.y={p.y}, p[0]={p[0]}")
    x, y = p  # tuple として unpack できる
    print(f"unpacked: x={x}, y={y}")


if __name__ == "__main__":
    main()
