"""decorator は「関数を受け取り、関数を返す」仕組み。

このファイルで扱うのは次の 2 点:

1. 自作 decorator `trace` を定義する（関数を引数にとり、ラップした関数を返す）
2. `@trace` を関数定義の上に書くと「`build_message = trace(build_message)`」と同じ意味になる

おまけで、自作 decorator では元関数のメタ情報（`__name__` など）を保つために
標準ライブラリの `@functools.wraps` を内側で使うのが定番、という話も含めている。

Java の annotation `@Override` などと違い、Python の decorator は **実行時に関数を
書き換える普通のコード** であって、メタ情報の付与だけではない点に注意。
"""

# ============================================================
# import 構文と命名規則の読み解き
# ============================================================
# `from X import Y` の意味:
#   1. モジュール X 全体を読み込み・実行する（中の他の名前もメモリには載る）
#   2. その中の名前 Y だけを **このファイルの名前空間に束縛** する
#   → 「メモリ節約のために 1 つだけロード」ではなく「短い名前で呼べるようにする」構文
#
# `from collections.abc import Callable` の構造:
#   - `collections`     : パッケージ（ディレクトリ）
#   - `collections.abc` : その中のサブモジュール（ドットはディレクトリ階層を辿る）
#   - `Callable`        : サブモジュールの中で定義されているクラス
#
# 命名規則（PEP 8、import される実体の種類が分かる）:
#   - CapWords (頭大文字)  → クラス        : `Callable`, `TypeVar`
#   - snake_case (頭小文字) → 関数 / 変数  : `wraps`, `perf_counter`
#   - UPPER_SNAKE          → 定数
#   Java や TypeScript の camelCase（先頭小文字の連結語）は Python では基本使わない。
#   このため「頭文字を見ただけでクラスか関数かほぼ判別できる」のが Python の利点。
#
# 下の 4 行を分類するとこうなる:
#   Callable      クラス    （Callable[[int], str] のように使う型ヒント）
#   wraps         関数      （@wraps(func) でデコレーター内に使う）
#   perf_counter  関数      （高精度な経過時間を返す）
#   TypeVar       クラス    （T = TypeVar("T") のようにインスタンス化する）
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import TypeVar


F = TypeVar("F", bound=Callable[..., object])


# ============================================================
# 自作 decorator の定義
# ============================================================
# decorator の正体: 「関数を引数として受け取り、別の関数を返す関数」
#
# trace は「呼び出しの前後にログ出力と所要時間計測を差し込んだ別の関数を返す」
# decorator として作っている。
def trace(func: F) -> F:
    # 内側で「ラップ後の新しい関数」を作って返す。これが decorator の典型形。
    @wraps(func)  # ← これも decorator。元関数のメタ情報（__name__, __doc__ 等）を wrapper にコピーする。
                  #   付けないと build_message.__name__ が "wrapper" になってしまう。
    def wrapper(*args: object, **kwargs: object) -> object:
        # *args / **kwargs は「任意の位置引数 / キーワード引数を全部受ける」記法。
        # これにより trace は「どんなシグネチャの関数でも」ラップできる。
        start = perf_counter()
        try:
            print(f"call {func.__name__}")
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (perf_counter() - start) * 1000
            print(f"done {func.__name__}: {elapsed_ms:.2f}ms")

    return wrapper  # type: ignore[return-value]


# ============================================================
# decorator の適用
# ============================================================
# `@trace` はシンタックスシュガー。次の 2 つはほぼ同じ意味:
#
#   @trace
#   def build_message(name: str) -> str:
#       return f"hello, {name}"
#
#   ↓ シンタックスシュガーを展開すると
#
#   def build_message(name: str) -> str:
#       return f"hello, {name}"
#   build_message = trace(build_message)
#
# つまり「`build_message` という名前は、もう元の関数ではなく `wrapper` を指す」状態になる。
# 以降このファイルから build_message を呼ぶと、wrapper が実行され、その中で元の関数が呼ばれる。
@trace
def build_message(name: str) -> str:
    return f"hello, {name}"


def main() -> None:
    # build_message("alice") を呼ぶと:
    #   1. wrapper が起動して "call build_message" を出力
    #   2. wrapper が中で元の build_message を呼び、"hello, alice" を取得
    #   3. wrapper が "done build_message: x.xx ms" を出力して結果を返す
    print(build_message("alice"))

    # @wraps が無いと、build_message.__name__ は "wrapper" になってしまう。
    # @wraps のおかげで元の関数名 "build_message" が保たれていることを確認。
    print(f"function name kept by wraps: {build_message.__name__}")


if __name__ == "__main__":
    main()
