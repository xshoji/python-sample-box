"""type hints は実行時チェックではない。

Python の型ヒントは、エディタ、型チェッカー、読み手のための情報です。
通常の実行時には自動で型検査されません。
"""

from typing import get_type_hints


def repeat(text: str, times: int) -> str:
    return text * times


def main() -> None:
    print(repeat("ha", 3))

    # 型ヒントには反しているが、Python として実行可能ならそのまま動く。
    print(repeat(["ha"], 3))  # type: ignore[arg-type]

    print(get_type_hints(repeat))


if __name__ == "__main__":
    main()
