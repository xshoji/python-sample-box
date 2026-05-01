"""`None`、truthiness、`is` と `==`。

Python では空の list / dict / str、0、None などが falsy です。
また、`None` との比較は値の等価性 `==` ではなく、同一性 `is` を使うのが慣例です。
"""


class WeirdNoneLike:
    def __eq__(self, other: object) -> bool:
        # 悪い例: == はクラス側で自由に振る舞いを変えられる。
        return other is None


def describe(value: object) -> str:
    if value is None:
        return "value is actually None"

    if not value:
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
