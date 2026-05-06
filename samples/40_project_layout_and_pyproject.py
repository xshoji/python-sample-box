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
    print("\n小さいアプリでは分かりやすいが、作業ディレクトリの package を誤って import しやすい。")

    print("\n--- src layout ---")
    print(SRC_LAYOUT)
    print("\nsrc/ 配下を install して使う前提なので、配布物に近い形で import を確認しやすい。")

    print("\n--- pyproject.toml の最小イメージ ---")
    print(PYPROJECT_EXAMPLE)
    print("\n現代の Python では、依存・メタ情報・ビルド設定を pyproject.toml に集約する流れ。")


if __name__ == "__main__":
    main()
