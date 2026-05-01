"""mutable object とデフォルト引数の罠。

Python のデフォルト引数は「関数定義時に一度だけ」評価されます。
list / dict のような mutable object をそのまま置くと、呼び出し間で共有されます。
"""

from __future__ import annotations


def append_bad(item: str, bucket: list[str] = []) -> list[str]:
    # 悪い例: bucket は呼び出しごとに新規作成されない。
    bucket.append(item)
    return bucket


def append_good(item: str, bucket: list[str] | None = None) -> list[str]:
    # Python では None を sentinel として使い、関数内で新しい list を作るのが定番。
    if bucket is None:
        bucket = []

    bucket.append(item)
    return bucket


def shallow_copy_example() -> None:
    original = [["apple"], ["banana"]]
    copied = original.copy()
    copied[0].append("cherry")

    # list.copy() は shallow copy。内側の list は共有されたまま。
    print(f"original = {original}")
    print(f"copied   = {copied}")


def main() -> None:
    print(append_bad("first"))
    print(append_bad("second"))

    print(append_good("first"))
    print(append_good("second"))

    shallow_copy_example()


if __name__ == "__main__":
    main()
