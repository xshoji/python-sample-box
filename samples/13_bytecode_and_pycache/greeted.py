"""main.py から import される側のモジュール。

このファイルが import されるたびに、CPython は対応するバイトコードを
``__pycache__/greeted.cpython-312.pyc`` に保存する（既にあれば再利用する）。
"""

print("greeted.py was imported")  # 副作用は import 時に 1 回だけ走ることを確認するための print


def greet(name: str) -> str:
    return f"hello, {name}"
