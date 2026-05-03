"""`None`、truthiness、`is` と `==`。

Python では空の list / dict / str、0、None などが falsy です。
また、`None` との比較は値の等価性 `==` ではなく、同一性 `is` を使うのが慣例です。
"""


class WeirdNoneLike:
    def __eq__(self, other: object) -> bool:
        # 悪い例: == はクラス側で自由に振る舞いを変えられる。
        return other is None


# 比較演算子の使い分けまとめ:
#
#   ==  : 値の等価性。`__eq__` がクラス側で定義されていればそれが呼ばれる。
#         例) "abc" == "abc" → True、 [1, 2] == [1, 2] → True
#         クラスによっては嘘の結果を返すこともできる（下の WeirdNoneLike が実例）。
#
#   is  : 同一性（オブジェクトとして同じ実体か）。Python 内部では id(x) == id(y) と等価。
#         比較対象がシングルトン（None, True, False）のときに使うのが鉄則。
#         例) x is None  ← 慣用句。`x == None` は PEP 8 で非推奨（E711 警告）。
#
#   not : 論理否定。`not x` は x が「falsy」のときに True を返す。
#         Python の falsy は: None / False / 0 / 0.0 / "" / [] / {} / set() / 自作クラスで __bool__ が False を返すもの。
#         つまり `if not value:` は「value が空っぽ系か None なら真」という意味になる。
#
# 下の describe() では:
#   1) まず `is None` で「本物の None かどうか」を厳密に判定する（== だと嘘をつくクラスに騙される）。
#   2) 次に `not value` で「None ではないが空っぽ系の値か」を判定する。
#   3) どちらでもなければ truthy（中身のある値）。
def describe(value: object) -> str:
    if value is None:
        # `is` を使うのは「同一性」での比較。None はプログラム全体で 1 つしかない
        # シングルトンなので、is で比較すれば WeirdNoneLike のような偽装に騙されない。
        return "value is actually None"

    if not value:
        # `not` は「falsy なら True」。"" / [] / {} / 0 などをまとめて拾える。
        return "value is falsy, but not None"


    return "value is truthy"


def main() -> None:
    values = [None, "", [], {}, 0, "hello", [1, 2, 3]]
    for value in values:
        print(f"{value!r:>12}: {describe(value)}")

    weird = WeirdNoneLike()
    print(f"weird == None -> {weird == None}")  # noqa: E711 - 違いを見せるためのサンプル。
    print(f"weird is None -> {weird is None}")


if __name__ == "__main__":
    main()
