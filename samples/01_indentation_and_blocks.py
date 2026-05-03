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


# 戻り値の型ヒント `-> None` は、Java / TypeScript の `void` に相当する「戻り値がない関数」の表現。
# ただし Python の `None` は「型」だけでなく「値」でもあり、`return` を書かない関数も
# 実際には `None` を返している（`x = loop_does_not_create_scope()` とすると x は None になる）。
# 値としての `None` の挙動は samples/04_none_truthiness_identity.py で詳しく扱う。
def loop_does_not_create_scope() -> None:
    for number in [1, 2, 3]:
        last_seen = number

    # for の中で作られた last_seen も、同じ関数スコープなら参照できる。
    print(f"last_seen = {last_seen}")


def main() -> None:
    print(indentation_defines_blocks(92))
    loop_does_not_create_scope()


# `if __name__ == "__main__":` は Python の慣用句で、「このファイルが
# スクリプトとして直接実行されたときだけ中身を実行する」という意味。
#
# 仕組み:
#   - すべての .py ファイルは実行時に `__name__` という変数を持つ。
#   - `python 01_indentation_and_blocks.py` のように直接実行された場合、
#     `__name__` は文字列 "__main__" になる。
#   - 一方、別ファイルから `import 01_indentation_and_blocks` のように
#     import された場合、`__name__` は "01_indentation_and_blocks"
#     （モジュール名）になる。
#   - したがって、この if ブロックの中身は「直接実行のときだけ」走る。
#
# なぜ必要か:
#   - Python はファイルを import すると、トップレベルに書かれた処理が
#     その時点で全部実行されてしまう（Java のように main() だけ呼ばれる
#     わけではない）。
#   - 「ライブラリとしても import できるし、単体スクリプトとしても
#     実行できる」ファイルを書くには、実行時にだけ走らせたい処理を
#     この main guard の中に隔離する必要がある。
#
# Java / Go との対応:
#   - Java の `public static void main(String[] args)`、
#     Go の `func main()` に近い役割だが、Python では「特別な関数」では
#     なく「ただの if 文」で実現している点がポイント。
#
# 詳細と import 時の挙動の違いは samples/03_main_guard_and_imports.py で扱う。
if __name__ == "__main__":
    main()
