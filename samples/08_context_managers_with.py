"""`with` と context manager。

ファイル、ロック、DB 接続など「開始と終了が対になる処理」は context manager にできます。
`with` を抜けるとき、例外が発生していても `__exit__` が呼ばれます。
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager


# ====================================================================
# context manager とは何か
# ====================================================================
# context manager は「`with` 文と組み合わせて使えるオブジェクト」のこと。
# 特別な型ではなく、「ある約束事（プロトコル）を満たしていれば誰でも context manager」
# という Python の duck typing らしい仕組みになっている。
#
# その約束事 = 次の 2 つのメソッドを持っていること:
#
#   __enter__(self)          : `with` でブロックに入るときに呼ばれる
#   __exit__(self, exc_type, exc, tb)
#                            : ブロックを抜けるときに必ず呼ばれる（例外時も）
#
# 代表的な context manager:
#   - 組み込み: open() の戻り値（ファイル）、threading.Lock(), tempfile.TemporaryDirectory() など
#   - 標準ライブラリ: contextlib.suppress, contextlib.redirect_stdout など
#   - 外部ライブラリ: DB トランザクション、HTTP クライアント、テスト用フィクスチャ など
#
# 「自分で context manager を作る」方法は 2 つ:
#
#   (A) クラスに __enter__ / __exit__ を実装する         ← TraceBlock がこの形
#   (B) ジェネレータ関数に @contextmanager を付ける       ← temporary_setting がこの形
#
# 簡単な前後処理なら (B) のほうが短く書ける。状態を持たせたい/再利用したいなら (A)。
# ====================================================================


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
    # ====================================================================
    # `with` 文とは何か
    # ====================================================================
    # `with <式> as <変数>:` は「ブロックに入る前後で、決まった処理を必ず実行する」
    # ための構文。「開始処理 → ブロック実行 → 終了処理」をワンセットで書ける。
    #
    # 仕組み:
    #   1. <式> を評価して context manager オブジェクトを得る
    #   2. その __enter__() を呼ぶ。返り値は `as` 以降の変数に入る（省略可）
    #   3. ブロックを実行する
    #   4. ブロックを抜けるとき（正常終了でも例外でも）必ず __exit__() を呼ぶ
    #
    # よくある用途:
    #   - ファイルを開いて確実に閉じる:        with open("a.txt") as f: ...
    #   - ロックを取得して確実に解放する:      with lock: ...
    #   - DB / HTTP / トランザクションの管理:  with conn.begin(): ...
    #
    # try / finally で書くと毎回:
    #   r = open("a.txt")
    #   try:
    #       ... use r ...
    #   finally:
    #       r.close()
    # となるところを `with open("a.txt") as r:` の 1 行に圧縮できる。
    # 「リソースの解放忘れ」を構文レベルで防げるのが最大の利点。
    #
    # 他言語との対応:
    #   - C# の `using (var x = ...) { ... }`
    #   - Java の try-with-resources `try (var x = ...) { ... }`
    #   - Go の `defer` （こちらは関数末尾で実行されるので少し挙動が違う）
    #
    # context manager の作り方は 2 通り:
    #   (A) クラスに __enter__ / __exit__ を実装する     ← 下の TraceBlock
    #   (B) 関数に @contextmanager を付け、yield で前後を分ける  ← 下の temporary_setting

    # (A) クラス版: __enter__ で "enter:..." を、__exit__ で "exit:..." を出す。
    # ブロックの中で例外が起きても __exit__ は必ず呼ばれる。
    with TraceBlock("manual class"):
        print("inside block")

    # (B) @contextmanager 版: yield の前が __enter__、後ろが __exit__ に相当。
    # try / finally と組み合わせるのが定番（途中で例外が起きても restore が走るように）。
    with temporary_setting("mode", "debug"):
        print("run with temporary setting")


if __name__ == "__main__":
    main()
