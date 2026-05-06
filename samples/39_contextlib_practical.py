"""`contextlib` 応用: context manager を軽く作る・組み合わせる。

`with` 文の仕組みを自前 class で実装しなくても、標準ライブラリ `contextlib` で
実務上よくある後片付けパターンを簡潔に書ける。
"""

from collections.abc import Iterator
from contextlib import ExitStack, closing, contextmanager, suppress
from io import StringIO


@contextmanager
def section(name: str) -> Iterator[None]:
    print(f"[{name}] start")
    try:
        yield
    finally:
        print(f"[{name}] end")


class ClosableBuffer(StringIO):
    def close(self) -> None:
        print("buffer closed")
        super().close()


def main() -> None:
    print("--- @contextmanager ---")
    with section("load"):
        print("  loading...")

    print("\n--- suppress: 無視してよい例外を明示する ---")
    values = {"timeout": "10"}
    with suppress(KeyError):
        print(values["missing"])
    print("  missing key は無視して続行")

    print("\n--- closing: close() だけを持つ object を with 対応にする ---")
    with closing(ClosableBuffer("hello")) as buffer:
        print(buffer.read())

    print("\n--- ExitStack: context manager の数が動的な場合 ---")
    names = ["db", "cache"]
    with ExitStack() as stack:
        for name in names:
            stack.enter_context(section(name))
        print("  まとめて処理中")


if __name__ == "__main__":
    main()
