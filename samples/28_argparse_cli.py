"""`argparse` で CLI を作る。

Python の CLI ツールは標準ライブラリ `argparse` だけで十分書ける。
3rd party の click / typer も人気だが、まずは標準を押さえるのが定石。

このサンプルでは:

- 必須の位置引数（positional argument）
- 任意のオプション（`--name`、`-n` のような short / long）
- フラグ（`--verbose` / `--no-verbose`）
- 型変換（`type=int`）
- choices による値制限
- サブコマンド（`add` / `sub` のような git 風コマンド）

通常 `parser.parse_args()` は `sys.argv[1:]` を読むが、
このサンプルでは「直接実行で挙動が分かる」ように、引数を明示的に渡して何度か実行する。
"""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="greet-tool",
        description="挨拶を出力するデモ CLI",
    )
    # ============================================================
    # 位置引数: 必須
    # ============================================================
    parser.add_argument("name", help="挨拶する相手の名前")

    # ============================================================
    # オプション: -n / --count、デフォルト値あり、型変換
    # ============================================================
    # short flag (-n) と long flag (--count) を併記できる。
    # type=int を渡しておくと、argparse が文字列 -> int 変換を担当してくれる。
    # 失敗すると親切なエラーメッセージで終了する（自前で int() しなくてよい）。
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="挨拶を繰り返す回数（デフォルト: 1）",
    )

    # ============================================================
    # choices: 値を制限する
    # ============================================================
    parser.add_argument(
        "--lang",
        choices=["en", "ja", "fr"],
        default="ja",
        help="言語",
    )

    # ============================================================
    # フラグ: BooleanOptionalAction で --verbose / --no-verbose の両方を生成
    # ============================================================
    parser.add_argument(
        "--verbose",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="詳細出力を出す",
    )

    return parser


def build_subcommand_parser() -> argparse.ArgumentParser:
    """git 風サブコマンドのデモ。"""
    parser = argparse.ArgumentParser(prog="calc-tool")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="2 つの数を足す")
    add_p.add_argument("x", type=int)
    add_p.add_argument("y", type=int)

    sub_p = sub.add_parser("sub", help="2 つの数を引く")
    sub_p.add_argument("x", type=int)
    sub_p.add_argument("y", type=int)

    return parser


def greet(name: str, count: int, lang: str, verbose: bool) -> None:
    if verbose:
        print(f"  [verbose] name={name}, count={count}, lang={lang}")
    template = {"en": "Hello", "ja": "こんにちは", "fr": "Bonjour"}[lang]
    for _ in range(count):
        print(f"  {template}, {name}!")


def main() -> None:
    parser = build_parser()

    # ============================================================
    # 通常は parser.parse_args() （引数なし）で sys.argv を読むが、
    # このサンプルでは手動で引数リストを渡して何パターンか試す。
    # ============================================================
    print("--- 例1: 必須引数だけ ---")
    args = parser.parse_args(["Alice"])
    greet(**vars(args))

    print("\n--- 例2: --count と --lang を指定 ---")
    args = parser.parse_args(["Bob", "--count", "3", "--lang", "en"])
    greet(**vars(args))

    print("\n--- 例3: --verbose フラグ ---")
    args = parser.parse_args(["Charlie", "--lang", "fr", "--verbose"])
    greet(**vars(args))

    # ============================================================
    # 不正な引数を渡すとどうなるか
    # ============================================================
    # parse_args は通常エラー時に SystemExit を投げる（プロセス終了）。
    # ここでは exit_on_error=False に切り替えるのではなく、
    # try/except SystemExit で捕まえるのが手軽。
    print("\n--- 例4: choices に無い --lang ---")
    try:
        parser.parse_args(["Dave", "--lang", "de"])
    except SystemExit as e:
        print(f"  SystemExit code = {e.code}")

    # ============================================================
    # サブコマンド
    # ============================================================
    print("\n--- サブコマンド ---")
    sub_parser = build_subcommand_parser()
    args = sub_parser.parse_args(["add", "3", "4"])
    print(f"  add 3 4 -> {args.x + args.y}")
    args = sub_parser.parse_args(["sub", "10", "7"])
    print(f"  sub 10 7 -> {args.x - args.y}")


if __name__ == "__main__":
    main()
