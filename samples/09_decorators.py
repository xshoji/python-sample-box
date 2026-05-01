"""decorator は関数を受け取り、関数を返す仕組み。

`@decorator` は構文糖です。関数定義の直後に
`target = decorator(target)` と書くのに近い意味になります。
"""

from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import TypeVar


F = TypeVar("F", bound=Callable[..., object])


def trace(func: F) -> F:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        start = perf_counter()
        try:
            print(f"call {func.__name__}")
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (perf_counter() - start) * 1000
            print(f"done {func.__name__}: {elapsed_ms:.2f}ms")

    return wrapper  # type: ignore[return-value]


@trace
def build_message(name: str) -> str:
    return f"hello, {name}"


def main() -> None:
    print(build_message("alice"))
    print(f"function name kept by wraps: {build_message.__name__}")


if __name__ == "__main__":
    main()
