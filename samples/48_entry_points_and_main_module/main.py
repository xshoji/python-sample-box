"""Python の実行入口: file.py、`-m`、`__main__.py`、console script。

Python では同じコードでも「ファイルとして実行する」のか「モジュールとして実行する」のかで、
`__name__` や import 探索の見え方が変わる。ここでは代表的な入口を概念として確認する。
"""

import runpy

from demo_pkg import cli


LAYOUT = """
samples/48_entry_points_and_main_module/
  main.py
  demo_pkg/
    __init__.py
    __main__.py      # python -m demo_pkg で実行される入口
    cli.py           # console script から呼ばれる関数を置く想定
""".strip()


def main() -> None:
    print("--- このサンプルの構成 ---")
    print(LAYOUT)

    print("\n--- 1. ファイルとして実行 ---")
    print("python samples/48_entry_points_and_main_module/main.py")
    print("  このファイルの if __name__ == '__main__' が入口になる")

    print("\n--- 2. 関数を直接呼ぶ ---")
    cli.main("direct call from main.py")

    print("\n--- 3. package を -m で実行するイメージ ---")
    print("python -m demo_pkg")
    print("  package の demo_pkg/__main__.py が実行される")
    runpy.run_module("demo_pkg", run_name="__main__")

    print("\n--- 4. pyproject.toml の console script は概念としては関数への別名 ---")
    print('[project.scripts]')
    print('demo-command = "demo_pkg.cli:main"')
    print("  install 後に demo-command を実行すると demo_pkg.cli.main が呼ばれる")


if __name__ == "__main__":
    main()
