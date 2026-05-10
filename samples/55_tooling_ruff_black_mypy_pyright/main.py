"""Python 開発ツールの位置づけ: formatter / linter / type checker。

このサンプルではツール自体は導入しない。Python 業務コードでよく見る Ruff、Black、
mypy、pyright が何を担当する道具なのかを、標準出力で確認する。
"""


TOOLS = [
    ("Black", "formatter", "コードの見た目を自動整形する"),
    ("Ruff", "linter / formatter", "未使用 import、PEP 8 系ルール、簡易整形などを高速にチェックする"),
    ("mypy", "type checker", "型ヒントを静的解析して、型の不整合を検出する"),
    ("pyright", "type checker", "型ヒントを静的解析する。VS Code / Pylance 系でもよく見る"),
]


def main() -> None:
    print("--- Python 開発ツールの役割 ---")
    for name, category, description in TOOLS:
        print(f"{name:7} | {category:18} | {description}")

    print("\n--- 使い分けのイメージ ---")
    print("formatter   : 人間が悩む整形を機械に任せる")
    print("linter      : バグの匂い、未使用コード、スタイル逸脱を見つける")
    print("type checker: type hints を元に、実行前に型の矛盾を見つける")

    print("\nこのリポジトリでは標準ライブラリ縛りのため、設定ファイルや依存追加はしない")


if __name__ == "__main__":
    main()
