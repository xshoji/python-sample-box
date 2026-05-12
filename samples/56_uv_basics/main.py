"""uv の基本操作: Python 本体・venv・依存・実行をまとめて扱う。

uv は標準ライブラリではないため、このサンプルでは実際に uv を呼び出さない。
代わりに、よく使うコマンドと役割を標準出力で確認する。
"""


COMMANDS = [
    ("uv python install 3.12", "Python 3.12 系をユーザー領域にインストールする"),
    ("uv init", "pyproject.toml を持つ新規プロジェクトを作る"),
    ("uv add requests", "依存を追加し、pyproject.toml と uv.lock を更新する"),
    ("uv run python main.py", "プロジェクトの仮想環境でコマンドを実行する"),
    ("uv sync", "uv.lock に従って仮想環境を再現する"),
    ("uv lock", "依存解決だけを行い、uv.lock を更新する"),
    ("uv tool run ruff check .", "プロジェクト外の CLI ツールを一時環境で実行する"),
]


def main() -> None:
    print("--- uv の位置づけ ---")
    print("uv は Python 本体の管理、venv 作成、依存解決、lock、実行をまとめて扱うツール")
    print("pip + venv + pip-tools + pyenv + pipx の一部を、1 つの高速な CLI に寄せたもの")

    print("\n--- よく使うコマンド ---")
    for command, description in COMMANDS:
        print(f"{command:28} # {description}")

    print("\n--- 覚え方 ---")
    print("uv add  : 依存を追加する")
    print("uv run  : そのプロジェクトの環境で実行する")
    print("uv sync : lock ファイルから環境を再現する")
    print("uv.lock : npm の package-lock.json に近い、再現性のためのファイル")


if __name__ == "__main__":
    main()
