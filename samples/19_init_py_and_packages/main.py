"""`__init__.py` と Python の package の挙動を確認するサンプル。

ディレクトリ構成:

    samples/19_init_py_and_packages/
        main.py                  ← このファイル（エントリポイント）
        mypkg/
            __init__.py          ← package の入口。初期化コード + 公開 API curation
            core.py              ← 公開クラス・関数を置く
            helpers.py           ← __init__.py 経由では公開していない内部用
            sub/
                __init__.py      ← サブ package の入口
                deep.py          ← さらに奥のモジュール

他言語との対応:
- Java: package 宣言と物理ディレクトリが一致するだけで、Python のような
        「package 初期化ファイル」は存在しない。
- Go  : 同じディレクトリの .go ファイルが暗黙に同一 package。
        `init()` 関数で初期化コードを書くという仕組みは Python の __init__.py に近い。
- JS  : Node.js の `index.js` が役割として近い（ディレクトリを require/import するときの入口）。

このスクリプトを実行する Python は、スクリプトの置かれているディレクトリを
sys.path[0] に自動で入れる。そのため `import mypkg` でこの dir 配下の
mypkg/ を見つけられる（=「このサンプルは追加設定なしでそのまま動く」）。
"""

from __future__ import annotations

import sys


def main() -> None:
    # ====================================================================
    # 1. package の初回 import — __init__.py が走るタイミング
    # ====================================================================
    print("# 1. import mypkg (初回)")
    import mypkg  # ← この瞬間に mypkg/__init__.py が実行される

    # ====================================================================
    # 2. 2 回目以降の import は __init__.py を再実行しない
    # ====================================================================
    # Python は一度 import したモジュールを sys.modules にキャッシュする。
    # 再 import しても __init__.py のメッセージは出ない。
    print("\n# 2. import mypkg (2 回目, 再実行されない)")
    import mypkg  # noqa: F811  # 同じ名前で再 import しても初期化は走らない
    print(f"  mypkg in sys.modules? {('mypkg' in sys.modules)}")

    # ====================================================================
    # 3. __init__.py が再エクスポートした「公開 API」へのフラットアクセス
    # ====================================================================
    # mypkg/__init__.py の中で `from .core import Greeter, greet` しているおかげで、
    # 利用者は mypkg.core という内部構造を知らずに mypkg 直下から触れる。
    print("\n# 3. 公開 API への access")
    print(f"  mypkg.__version__ = {mypkg.__version__}")
    print(f"  mypkg.greet('alice') = {mypkg.greet('alice')!r}")
    g = mypkg.Greeter(prefix="Hi")
    print(f"  mypkg.Greeter(prefix='Hi').say('bob') = {g.say('bob')!r}")

    # ====================================================================
    # 4. __all__ の効き方
    # ====================================================================
    # __all__ は `from mypkg import *` のときの「拾う対象」を制御する。
    # `from mypkg import name` の単発 import には影響しないので、
    # __all__ は「公開シンボルの宣言」であって「アクセス制御」ではない。
    print("\n# 4. __all__ の中身（star import の対象）")
    print(f"  mypkg.__all__ = {mypkg.__all__}")

    # ====================================================================
    # 5. 「公開していない」内部モジュールにも、パスを書けばアクセスできる
    # ====================================================================
    # mypkg.helpers は __init__.py から再エクスポートしていないし、__all__ にも無い。
    # それでも `mypkg.helpers` というモジュールパスは生きており、import できてしまう。
    # → Python に真のプライベートは無く、慣習（_ 始まりの名前など）で守るしかない。
    print("\n# 5. 公開していない内部モジュールへの直接アクセス")
    from mypkg.helpers import internal_helper
    print(f"  mypkg.helpers.internal_helper(21) = {internal_helper(21)}")

    # ====================================================================
    # 6. サブ package の import
    # ====================================================================
    # mypkg.sub は別の __init__.py を持つ独立した package。
    # 初めて触ったタイミングで mypkg/sub/__init__.py が実行される。
    print("\n# 6. サブ package を import すると、その __init__.py が走る")
    from mypkg.sub import deep
    print(f"  deep.deep_function() = {deep.deep_function()!r}")

    # ====================================================================
    # 7. パッケージ自体は「モジュールオブジェクト」である
    # ====================================================================
    # import 文で取れる package は、内部的にはモジュールオブジェクトの一種。
    # __file__ で実体ファイルの場所が分かり、__path__ で package のディレクトリが分かる。
    print("\n# 7. mypkg のモジュールオブジェクトとしての姿")
    print(f"  type(mypkg)  = {type(mypkg).__name__}")
    print(f"  mypkg.__file__ ends with: ...{mypkg.__file__[-40:]}")
    print(f"  mypkg.__path__ = {list(mypkg.__path__)[0][-40:]!r} (末尾 40 文字)")


if __name__ == "__main__":
    main()
