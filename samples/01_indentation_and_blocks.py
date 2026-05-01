"""インデントは見た目ではなく、Python の構文そのもの。

Java / Go / JavaScript の `{ ... }` に相当するものを、Python では
インデントで表します。ただし if / for / with などは新しいローカル
スコープを作りません。
"""


def indentation_defines_blocks(score: int) -> str:
    if score >= 80:
        message = "passed with room to spare"
        print("この print は if ブロックの中")
    else:
        message = "needs another try"
        print("この print は else ブロックの中")

    # if ブロックで代入した message は、この関数スコープ内で使える。
    # Python の if / for は JavaScript の let ブロックスコープのようには振る舞わない。
    return message


def loop_does_not_create_scope() -> None:
    for number in [1, 2, 3]:
        last_seen = number

    # for の中で作られた last_seen も、同じ関数スコープなら参照できる。
    print(f"last_seen = {last_seen}")


def main() -> None:
    print(indentation_defines_blocks(92))
    loop_does_not_create_scope()


if __name__ == "__main__":
    main()
