"""iterable / iterator / generator。

Python の for 文は「添字で回す構文」ではなく、iterable protocol を使います。
generator は値を一度に全て作らず、必要になった分だけ `yield` します。
"""

from collections.abc import Iterator


def count_up_to(limit: int) -> Iterator[int]:
    current = 1
    while current <= limit:
        print(f"yielding {current}")
        yield current
        current += 1


def main() -> None:
    # count_up_to(3) は generator object を返す。この時点ではまだ何も実行されていない
    # （`yielding 1` などは出ない）。next() か for で値を取り出した瞬間に動き出す。
    counter = count_up_to(3)

    print("generator object was created")
    print(next(counter))   # 1 を取り出す（"yielding 1" が先に出力される）
    print(next(counter))   # 2 を取り出す

    print("remaining values are consumed by for")
    # generator は途中まで next() で消費した状態を覚えている。
    # ここでは「3 だけ残っている」状態から for を回すので、3 だけが出力される。
    for value in counter:
        print(value)

    # generator expression: list 内包表記 [...] と同じ構文を () で書いたもの。
    # list と違い、中身を全部メモリに作らず、要求されたタイミングで 1 つずつ計算する。
    # 大きなデータを扱うときにメモリ節約になる。
    squares = (n * n for n in range(1, 4))
    print(f"generator expression = {squares}")            # <generator object ...> のような表示
    print(f"materialized list = {list(squares)}")        # list() で全部消費 → [1, 4, 9]


if __name__ == "__main__":
    main()
