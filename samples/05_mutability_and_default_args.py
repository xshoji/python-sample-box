"""mutable object とデフォルト引数の罠。

Python のデフォルト引数は「関数定義時に一度だけ」評価されます。
list / dict のような mutable object をそのまま置くと、呼び出し間で共有されます。
"""


def append_bad(item: str, bucket: list[str] = []) -> list[str]:
    # 悪い例: bucket は呼び出しごとに新規作成されない。
    bucket.append(item)
    return bucket


# 引数 `bucket: list[str] | None = None` の構文を分解すると次の 4 要素から成る:
#
#   bucket          : 引数名
#   : list[str] | None  : 型ヒント（後述）
#   = None          : デフォルト値（呼び出し側が省略したときに使われる値）
#
# 型ヒント部分のさらなる分解:
#
#   list[str]
#     - 「str を要素に持つ list」を表すパラメータ化された型ヒント。
#     - Python 3.9+ では組み込みの list / dict / tuple がそのまま [] を取れる。
#     - 3.8 以前は `from typing import List` して `List[str]` と書く必要があった。
#     - Java の `List<String>`、TypeScript の `string[]` に相当。
#
#   |（パイプ）
#     - 型同士の Union（「A もしくは B」）を表す。Python 3.10+ で導入。
#     - `list[str] | None` は「list[str] か、None のどちらか」を意味する。
#     - 古い書き方では `Optional[list[str]]`（= `Union[list[str], None]`）。
#     - TypeScript の `string[] | null`、Kotlin の `List<String>?` に相当。
#
# 型ヒントは Python の実行時に評価されるが、値の型を強制するためではなく、
# エディタ補完や mypy / pyright 等の静的解析のための情報、というのが Python の立場。
# 詳細は samples/11_type_hints_are_not_runtime_checks.py を参照。
#
# デフォルト値に `None` を使うのは、上の append_bad の罠（mutable な
# デフォルト値が呼び出し間で共有される）を避けるための定石。
# 「未指定」を表す sentinel として None を受け取り、関数内で新しい list を作る。
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
    # --- append_bad: mutable デフォルト引数の罠 ---
    # 呼び出しごとに新しい list ができそうに見えるが、関数定義時に評価された
    # 1 つの list が共有されるため、2 回目以降に過去の値が残ってしまう。
    print("append_bad (bucket 省略):")
    print(f"  1回目: {append_bad('first')}")    # → ['first']
    print(f"  2回目: {append_bad('second')}")   # → ['first', 'second']  ← 残ってる！

    # --- append_good: bucket を渡さない場合 ---
    # bucket=None で呼ばれるので、関数内で毎回新しい list を作る。
    # → 呼び出し間で値が共有されない（append_bad との違い）。
    print("\nappend_good (bucket 省略):")
    print(f"  1回目: {append_good('first')}")   # → ['first']
    print(f"  2回目: {append_good('second')}")  # → ['second']  ← クリーンに分離されている

    # --- append_good: bucket を明示的に渡す場合 ---
    # 既存の list に追加したい、というユースケース。
    # `if bucket is None:` のチェックがあるおかげで、渡された list はそのまま使われる。
    # もしチェックが無く `bucket = []` だけだったら、existing が捨てられて
    # 結果は ['cherry'] になってしまう（呼び出し側が渡した意味が無くなる）。
    print("\nappend_good (既存の bucket を渡す):")
    existing = ["apple", "banana"]
    result = append_good("cherry", bucket=existing)
    print(f"  result   = {result}")     # → ['apple', 'banana', 'cherry']
    print(f"  existing = {existing}")   # → ['apple', 'banana', 'cherry']  ← 同じ list を更新している

    print()
    shallow_copy_example()


if __name__ == "__main__":
    main()
