"""iterable / iterator / generator。

Python の for 文は「添字で回す構文」ではなく、iterable protocol を使います。
generator は値を一度に全て作らず、必要になった分だけ `yield` します。
"""

from collections.abc import Iterator


def count_up_to(limit: int) -> Iterator[int]:
    current = 1
    while current <= limit:
        print(f"yielding {current}")
        yield current
        current += 1


def main() -> None:
    numbers = count_up_to(3)

    print("generator object was created")
    print(next(numbers))
    print(next(numbers))

    print("remaining values are consumed by for")
    for number in numbers:
        print(number)

    squares = (number * number for number in range(1, 4))
    print(f"generator expression = {squares}")
    print(f"materialized list = {list(squares)}")


if __name__ == "__main__":
    main()
