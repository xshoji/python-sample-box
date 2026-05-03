"""`__init__` と dunder method。

dunder は "double underscore" の略です。`__init__`、`__repr__`、
`__len__` のような名前は、Python の構文や組み込み関数から呼ばれる
特別なフックです。
"""


class Cart:
    def __init__(self, owner: str) -> None:
        # `__init__` はコンストラクタそのものではなく、生成済みインスタンスの初期化フック。
        # 実際の生成は `__new__` が担当するが、通常は意識しない。
        self.owner = owner
        self.items: list[str] = []

    def add(self, item: str) -> None:
        self.items.append(item)

    def __len__(self) -> int:
        # len(cart) から呼ばれる。
        return len(self.items)

    def __contains__(self, item: str) -> bool:
        # `item in cart` から呼ばれる。
        return item in self.items

    def __repr__(self) -> str:
        # デバッグ時に「再現しやすい表現」を返すのが慣例。
        # 先頭の `f` は f-string (formatted string literal, Python 3.6+)。
        # `{}` の中に式を書くとその場で評価されて文字列に埋め込まれる。
        # JavaScript の `` `hello, ${name}` ``、Kotlin の "$name" 相当。
        #
        # `{値}` だけだとデフォルトで str() が使われ、文字列はクォートなしでそのまま埋め込まれる。
        #   例) f"{'alice'}"   → alice
        # `!r` を付けると repr() が使われ、文字列であることが分かる形（クォート付き）で埋め込まれる。
        #   例) f"{'alice'!r}" → 'alice'
        # __repr__ の中では「再現可能な表現」が欲しいので慣例的に `!r` を使う。
        # 他に `!s` (= str)、`!a` (= ascii) があり、`:` の後ろでは書式指定（例: f"{x:.2f}"）も使える。
        return f"Cart(owner={self.owner!r}, items={self.items!r})"


def main() -> None:
    cart = Cart("alice")
    cart.add("book")
    cart.add("pen")

    print(cart)
    print(f"len(cart) = {len(cart)}")
    print(f"'book' in cart = {'book' in cart}")


if __name__ == "__main__":
    main()
