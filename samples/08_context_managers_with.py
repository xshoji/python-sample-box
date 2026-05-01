"""`with` と context manager。

ファイル、ロック、DB 接続など「開始と終了が対になる処理」は context manager にできます。
`with` を抜けるとき、例外が発生していても `__exit__` が呼ばれます。
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager


class TraceBlock:
    def __init__(self, label: str) -> None:
        self.label = label

    def __enter__(self) -> "TraceBlock":
        print(f"enter: {self.label}")
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: object) -> bool:
        print(f"exit : {self.label}")
        # False を返すと、発生した例外は握りつぶされず呼び出し元へ伝播する。
        return False


@contextmanager
def temporary_setting(name: str, value: str) -> Iterator[None]:
    print(f"set {name}={value}")
    try:
        yield
    finally:
        print(f"restore {name}")


def main() -> None:
    with TraceBlock("manual class"):
        print("inside block")

    with temporary_setting("mode", "debug"):
        print("run with temporary setting")


if __name__ == "__main__":
    main()
