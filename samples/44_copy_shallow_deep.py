"""Java 経験者向け: Python の shallow copy / deep copy で注意する点。

「変数代入はコピーではなく参照共有」という点は、Java の List / Map と同じ感覚でよい。
Python で特に意識したいのは、`list.copy()` や `copy.copy()` は shallow copy なので、
ネストした list / dict や dataclass の mutable field までは複製しないこと。
"""

import copy
from dataclasses import dataclass, field


@dataclass
class Cart:
    owner: str
    items: list[str] = field(default_factory=list)


def main() -> None:
    print("--- 1. 代入はコピーではない（Java の List 参照と同じ感覚） ---")
    original = ["apple", "banana"]
    alias = original
    alias.append("cherry")
    print(f"original: {original}")
    print(f"alias is original: {alias is original}")

    print("\n--- 2. Python の list.copy() は shallow copy ---")
    nested = [["apple"], ["banana"]]
    shallow = nested.copy()
    shallow.append(["cherry"])
    shallow[0].append("avocado")
    print(f"nested : {nested}")
    print(f"shallow: {shallow}")
    print(f"shallow is nested: {shallow is nested}")
    print(f"shallow[0] is nested[0]: {shallow[0] is nested[0]}")
    print("  外側の list は別でも、中の list は共有される")

    print("\n--- 3. copy.deepcopy() は中のオブジェクトも再帰的にコピー ---")
    deep = copy.deepcopy(nested)
    deep[0].append("apricot")
    print(f"nested: {nested}")
    print(f"deep  : {deep}")
    print(f"deep[0] is nested[0]: {deep[0] is nested[0]}")
    print("  便利だが、巨大な構造ではコストや意図しない複製に注意する")

    print("\n--- 4. dataclass でも copy.copy() は shallow copy ---")
    cart = Cart(owner="alice", items=["book"])
    copied_cart = copy.copy(cart)
    copied_cart.items.append("pen")
    print(f"cart.items       : {cart.items}")
    print(f"copied_cart.items: {copied_cart.items}")
    print("  Cart オブジェクト自体は別でも、items list は共有される")
    print("  Python では list / dict を field に持つ dataclass が多いので、ここが実務上の注意点")


if __name__ == "__main__":
    main()
