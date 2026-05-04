"""mypkg の中核モジュール。

`__init__.py` から再エクスポートされる「公開 API」をここに置いている。
利用者はこのファイルの存在を意識せず `from mypkg import Greeter, greet` で使える。
"""

from __future__ import annotations


class Greeter:
    """挨拶を組み立てるクラス（中身は重要ではなく、再エクスポートされることが本題）。"""

    def __init__(self, prefix: str = "Hello") -> None:
        self.prefix = prefix

    def say(self, name: str) -> str:
        return f"{self.prefix}, {name}!"


def greet(name: str) -> str:
    """関数も同じく公開 API。"""
    return Greeter().say(name)
