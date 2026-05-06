"""`itertools` / `functools` 厳選: 反復処理を部品として組み立てる。

Python では iterator を返す小さな部品を組み合わせると、メモリ効率よく
データ処理を書ける。標準ライブラリの中でも OSS でよく見かけるものを扱う。
"""

from functools import cache, partial, reduce
from itertools import accumulate, chain, groupby, pairwise
from operator import add


def itertools_example() -> None:
    print("--- chain: 複数 iterable をつなぐ ---")
    print(list(chain([1, 2], [3, 4], [5])))

    print("\n--- pairwise: 隣り合う要素を見る ---")
    days = ["Mon", "Tue", "Wed", "Thu"]
    print(list(pairwise(days)))

    print("\n--- accumulate: 累積値 ---")
    sales = [100, 200, 50]
    print(list(accumulate(sales)))

    print("\n--- groupby: 連続する同じ key をまとめる ---")
    # key は「何を基準に並べる / まとめるか」を返す関数。
    # lambda row: row[0] は、("tokyo", "alice") のような tuple から 0 番目の city を取り出す無名関数。
    # JavaScript なら (row) => row[0]、Java なら Comparator.comparing(row -> row[0]) に近い。
    rows = sorted(
        [("tokyo", "alice"), ("osaka", "bob"), ("tokyo", "carol")],
        key=lambda row: row[0],
    )
    # groupby は「隣り合っている同じ key」だけをまとめるので、事前に同じ key で sorted しておくのが定番。
    for city, group in groupby(rows, key=lambda row: row[0]):
        print(city, [name for _, name in group])


# `@cache` は `fibonacci = cache(fibonacci)` とほぼ同じ意味の decorator。
# 同じ引数で呼ばれたとき、関数本体を再実行せず、前回の戻り値を再利用する。
# そのため「同じ入力なら常に同じ結果を返す」関数で使うのが基本。
@cache
def fibonacci(n: int) -> int:
    # ここでは fibonacci(8) などが何度も必要になるため、cache がないと同じ計算を大量に繰り返す。
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def functools_example() -> None:
    print("\n--- partial: 一部の引数を固定する ---")
    add_tax = partial(lambda price, tax_rate: int(price * (1 + tax_rate)), tax_rate=0.10)
    print(add_tax(1000))

    print("\n--- cache: 結果をメモ化する ---")
    print(fibonacci(10))
    # cache_info() で「cache に当たった回数」「新しく計算した回数」などを確認できる。
    print(fibonacci.cache_info())

    print("\n--- reduce: 畳み込み（多くの場面では sum 等を優先） ---")
    print(reduce(add, [1, 2, 3, 4], 0))


def main() -> None:
    itertools_example()
    functools_example()


if __name__ == "__main__":
    main()
