"""type hints は実行時チェックではない。

Python の型ヒントは、エディタ、型チェッカー、読み手のための情報です。
通常の実行時には自動で型検査されません。
"""

from typing import get_type_hints


def repeat(text: str, times: int) -> str:
    return text * times


def main() -> None:
    # 1. 型ヒント通りに呼んだ正常系。
    print(repeat("ha", 3))                        # → 'hahaha'

    # 2. 型ヒントには反しているが、Python の演算としては成立するのでそのまま動いてしまう例。
    #    list * int はリスト反復演算として定義されているため、エラーにならず ['ha', 'ha', 'ha'] が返る。
    #    型ヒントは「正しさを実行時に保証してくれない」ことの分かりやすい証拠。
    #    `# type: ignore[arg-type]` は mypy 等の静的解析にだけ「ここの型不一致は意図的」と伝えるコメント。
    print(repeat(["ha"], 3))  # type: ignore[arg-type]

    # 3. 型ヒントに反していて、かつ Python の演算としても成立しないため実行時に落ちる例。
    #    times に str を渡すと、関数の中で実行される `text * times` が `"ha" * "x"` となり、
    #    str * str は未定義なので TypeError になる。
    #    つまり型ヒントは何もしてくれず、エラーが出るのは「実際にその式を評価したとき」だけ。
    try:
        print(repeat("ha", "x"))  # type: ignore[arg-type]
    except TypeError as exc:
        print(f"runtime TypeError: {exc}")

    # ============================================================
    # get_type_hints とは
    # ============================================================
    # 関数 / クラス / モジュールに付けた型ヒントを「dict として取り出す」ヘルパ。
    # 戻り値の形は {引数名: 型, "return": 戻り値型}。
    #
    # なぜ専用関数があるのか:
    #   - `repeat.__annotations__` でも型ヒント自体は取れるが、`from __future__ import annotations`
    #     や Python 3.x の挙動によっては「型が文字列のまま」入っていることがある。
    #   - get_type_hints はその文字列を実際の型オブジェクトに解決し、ForwardRef や Optional の
    #     正規化（int | None ↔ Optional[int]）も行ってくれる。
    #
    # 主な使い道:
    #   - 自作のフレームワークやシリアライザ（FastAPI, pydantic 等の内部はこの仕組みで型を読む）
    #   - dataclass や TypedDict と組み合わせたバリデーション
    #   - ジェネリックなデコレーターでのシグネチャ検査
    #
    # 通常のアプリコードで毎日使う API ではなく、「型ヒントを“実行時のメタ情報”として
    # 活用したいライブラリ作者向け」と理解しておけばよい。
    print(get_type_hints(repeat))                 # → {'text': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}


if __name__ == "__main__":
    main()
