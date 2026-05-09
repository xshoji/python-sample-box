"""Python 3.12 のジェネリクス構文（PEP 695）。

Python 3.12 では `def first[T](...)` や `class Box[T]` のように、
型変数を関数・クラス定義のすぐ横に書けるようになった。
型ヒントなので、実行時に値の型を強制するものではない。
"""

from typing import TypeVar


def first[T](items: list[T]) -> T:
    return items[0]


class Box[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value


OldStyleT = TypeVar("OldStyleT")


def old_style_first(items: list[OldStyleT]) -> OldStyleT:
    # Python 3.11 以前でよく見る TypeVar を使った書き方。
    return items[0]


def describe_pair[T, U](left: T, right: U) -> str:
    return f"left={left!r} ({type(left).__name__}), right={right!r} ({type(right).__name__})"


def main() -> None:
    print("--- 関数のジェネリクス ---")
    print(first([1, 2, 3]))
    print(first(["a", "b", "c"]))

    print("\n--- クラスのジェネリクス ---")
    int_box = Box(123)
    str_box = Box("hello")
    print(int_box.get())
    print(str_box.get())

    print("\n--- 旧来の TypeVar との比較 ---")
    print(old_style_first([10, 20]))

    print("\n--- 型ヒントは実行時チェックではない ---")
    print(describe_pair("id", 100))
    # Box[int] のつもりでも、実行時に str を入れること自体は Python が禁止しない。
    mixed_box: Box[int] = Box("not int")  # type checker なら警告対象になり得る。
    print(f"mixed_box.get(): {mixed_box.get()!r}")


if __name__ == "__main__":
    main()
