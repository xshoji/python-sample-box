"""mypkg の内部ヘルパー。

このモジュールは `__init__.py` から再エクスポートしていない（`__all__` にも入れていない）。
それでも `from mypkg.helpers import internal_helper` のように **モジュールパスを直接
指定すれば import できる** ことを示すためのサンプル。

→ Python では「真にプライベート」にする仕組みは無く、慣習で守るしかない。
   慣習: 名前を `_` で始める / ドキュメントで「内部用」と明記する。
"""


def internal_helper(value: int) -> int:
    """`__init__.py` 経由では公開していない関数。

    `from mypkg import internal_helper` は失敗するが、
    `from mypkg.helpers import internal_helper` は成功する。
    """
    return value * 2
