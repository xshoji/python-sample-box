"""ディレクトリ名・パッケージ名・import 探索起点の関係を確認する。

Java や PHP のように、Python ファイルの先頭で「自分はこの package / namespace に
所属する」と宣言する文法はない。Python では、ファイルが置かれたディレクトリ構造と
`sys.path` の探索起点によって import 名が決まる。

このサンプルでは `app_like_package/services/mail.py` が、コード内で所属パッケージを
宣言していないにもかかわらず `app_like_package.services.mail` として扱われることを確認する。
"""

import importlib.util
import sys
from pathlib import Path

import app_like_package
from app_like_package.services import mail


def show_import_roots() -> None:
    print("# 1. import 探索の起点")
    print(f"  現在の作業ディレクトリ: {Path.cwd()}")
    print(f"  sys.path[0]: {sys.path[0]}")
    print("  Python は sys.path に並んだ各ディレクトリを Root 候補として順に探す")


def show_package_names() -> None:
    print("\n# 2. ディレクトリ階層が import 名になる")
    print(f"  app_like_package.__name__: {app_like_package.__name__}")
    print(f"  mail.__name__: {mail.__name__}")
    print(f"  mail.__package__: {mail.__package__}")
    print(f"  mail.__file__: ...{mail.__file__[-60:]}")
    print(f"  mail.build_subject('alice'): {mail.build_subject('alice')!r}")


def show_resolution_candidate() -> None:
    print("\n# 3. import 名から実ファイルが見つかる")
    module_name = "app_like_package.services.mail"
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        raise RuntimeError(f"{module_name} が見つかりません")

    print(f"  import 名: {module_name}")
    print(f"  解決されたファイル: ...{str(spec.origin)[-60:]}")
    print("  先頭に `package app_like_package.services` のような宣言は書いていない")


def show_src_layout_note() -> None:
    print("\n# 4. `src/` レイアウトでの考え方")
    print("  project/src/my_app/services/mail.py がある場合、import 名は普通 `my_app.services.mail`")
    print("  `src` は import 名の一部ではなく、sys.path 側に入る探索起点として扱う")


def main() -> None:
    show_import_roots()
    show_package_names()
    show_resolution_candidate()
    show_src_layout_note()


if __name__ == "__main__":
    main()
