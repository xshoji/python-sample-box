"""代入・shallow copy・deep copy の違い。

Python の変数代入はオブジェクトのコピーではなく、同じオブジェクトへの参照を増やす。
ネストした list / dict では shallow copy と deep copy の違いがバグになりやすい。
"""

import copy
from dataclasses import dataclass, field


@dataclass
class Cart:
    owner: str
    items: list[str] = field(default_factory=list)


def main() -> None:
    print("--- 代入はコピーではない ---")
    original = ["apple", "banana"]
    alias = original
    alias.append("cherry")
    print(f"original: {original}")
    print(f"alias is original: {alias is original}")

    print("\n--- shallow copy は外側だけ別オブジェクト ---")
    nested = [["apple"], ["banana"]]
    shallow = copy.copy(nested)
    shallow.append(["cherry"])
    shallow[0].append("avocado")
    print(f"nested : {nested}")
    print(f"shallow: {shallow}")
    print(f"shallow is nested: {shallow is nested}")
    print(f"shallow[0] is nested[0]: {shallow[0] is nested[0]}")

    print("\n--- deep copy は中のオブジェクトも再帰的にコピー ---")
    deep = copy.deepcopy(nested)
    deep[0].append("apricot")
    print(f"nested: {nested}")
    print(f"deep  : {deep}")
    print(f"deep[0] is nested[0]: {deep[0] is nested[0]}")

    print("\n--- dataclass でも mutable field は共有に注意 ---")
    cart = Cart(owner="alice", items=["book"])
    copied_cart = copy.copy(cart)
    copied_cart.items.append("pen")
    print(f"cart.items       : {cart.items}")
    print(f"copied_cart.items: {copied_cart.items}")
    print("  Cart オブジェクト自体は別でも、items list は shallow copy では共有される")


if __name__ == "__main__":
    main()
