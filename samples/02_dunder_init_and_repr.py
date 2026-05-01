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
