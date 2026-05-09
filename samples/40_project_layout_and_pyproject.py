"""`pyproject.toml` と `src/` レイアウト: Python プロジェクト構成の基本。

実行するコードというより、現代的な Python プロジェクトでよく見るファイル配置を
標準出力で確認するサンプル。実際の設定ファイルは追加せず、概念だけを扱う。
"""


FLAT_LAYOUT = """
my_app/
  pyproject.toml
  my_app/
    __init__.py
    service.py
  tests/
    test_service.py
""".strip()


FLAT_LAYOUT_IMPORT_NOTE = """
flat layout では、プロジェクトルート直下に package ディレクトリがある。
そのため `cd my_app` してテストやスクリプトを実行すると、現在の作業ディレクトリ経由で
`import my_app` が成功しやすい。

これは小さいプロジェクトでは分かりやすい一方で、pyproject.toml の package 設定が
間違っていても「ローカルでは import できる」状態になり、配布物として正しく
インストールできるかを見落としやすい。
""".strip()


SRC_LAYOUT = """
my_app/
  pyproject.toml
  src/
    my_app/
      __init__.py
      service.py
  tests/
    test_service.py
""".strip()


PYPROJECT_EXAMPLE = """
[project]
name = "my-app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
my-app = "my_app.cli:main"
""".strip()


def main() -> None:
    print("--- flat layout ---")
    print(FLAT_LAYOUT)
    print(f"\n{FLAT_LAYOUT_IMPORT_NOTE}")

    print("\n--- src layout ---")
    print(SRC_LAYOUT)
    print("\nsrc/ 配下を install して使う前提なので、配布物に近い形で import を確認しやすい。")

    print("\n--- pyproject.toml の最小イメージ ---")
    print(PYPROJECT_EXAMPLE)
    print("\n現代の Python では、依存・メタ情報・ビルド設定を pyproject.toml に集約する流れ。")


if __name__ == "__main__":
    main()
