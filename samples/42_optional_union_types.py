"""`T | None` と `Union`: None を含む型の書き方。

Python 3.10 以降では、複数の型を受け取る値を `A | B` と書ける。
`Optional[T]` は「省略可能」という意味ではなく、型としては `T | None` と同じ。
"""

from typing import Optional, Union


def greeting(name: str | None) -> str:
    # `str | None` は「str か None」。None でないことを確認すると str として扱える。
    if name is None:
        return "こんにちは、ゲストさん"
    return f"こんにちは、{name.upper()} さん"


def legacy_greeting(name: Optional[str]) -> str:
    # Optional[str] は古くからある書き方で、意味は str | None と同じ。
    if name is None:
        return "hello, guest"
    return f"hello, {name.lower()}"


def parse_id(value: int | str) -> int:
    # `int | str` は Union[int, str] と同じ意味。
    if isinstance(value, int):
        return value
    return int(value)


def legacy_parse_id(value: Union[int, str]) -> int:
    return parse_id(value)


def connect(host: str = "localhost", timeout_seconds: int | None = None) -> str:
    # 「引数を省略できる」ことと「None を渡せる」ことは別。
    # host は省略できるが、型は str なので None を想定していない。
    # timeout_seconds は省略もできるし、明示的に None も渡せる。
    timeout_label = "既定値" if timeout_seconds is None else f"{timeout_seconds} 秒"
    return f"host={host}, timeout={timeout_label}"


def main() -> None:
    print("--- T | None ---")
    print(greeting("Alice"))
    print(greeting(None))

    print("\n--- Optional[T] は T | None と同じ意味 ---")
    print(legacy_greeting("BOB"))
    print(legacy_greeting(None))

    print("\n--- Union[A, B] と A | B ---")
    print(parse_id(123))
    print(parse_id("456"))
    print(legacy_parse_id("789"))

    print("\n--- 省略可能な引数と None を許す型は別 ---")
    print(connect())
    print(connect(timeout_seconds=None))
    print(connect(timeout_seconds=10))


if __name__ == "__main__":
    main()
