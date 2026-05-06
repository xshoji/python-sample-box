"""`subprocess.run` の正しい使い方。

Python から外部コマンドを呼ぶときは `subprocess.run` を使う。
業務では CLI ラッパー、バッチ、Git 操作、変換ツール呼び出しなどで頻出する。
"""

import shlex
import subprocess
import sys


def successful_command() -> None:
    print("--- capture_output=True, text=True ---")
    result = subprocess.run(
        [sys.executable, "-c", "print('hello from child')"],
        check=True,
        capture_output=True,
        text=True,
    )
    print(f"stdout={result.stdout.strip()!r}")


def failing_command() -> None:
    print("\n--- check=True は失敗時に例外 ---")
    try:
        subprocess.run(
            [sys.executable, "-c", "import sys; print('ng'); sys.exit(2)"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"returncode={error.returncode}, stdout={error.stdout.strip()!r}")


def shell_true_warning() -> None:
    print("\n--- shell=True は原則避ける ---")
    # shell=True は、指定した文字列を `/bin/sh` や `cmd.exe` のような shell に解釈させて実行する指定。
    # shell は `;`, `&&`, `|`, `>`, `$()` などを特別扱いするため、ユーザー入力を文字列連結すると危険。
    # 例: `echo file name; rm -rf /tmp/test1` は「echo した後に別コマンドを実行する」意味になってしまう。
    user_input = "file name; rm -rf /tmp/test1"
    # list で渡すと shell を経由せず、各要素がそのまま argv として渡る。
    # この場合 `; rm -rf /tmp/test1` はただの文字列引数であり、別コマンドとして解釈されない。
    safe_args = ["echo", user_input]
    print(f"安全: subprocess.run({safe_args!r}) のように list で渡す")
    # どうしても shell の機能（pipe や redirect など）が必要な場合だけ shell=True を検討する。
    # その場合も、外部入力は shlex.quote などで shell 用にエスケープする。
    print(f"どうしても shell 用文字列を作るなら quote: echo {shlex.quote(user_input)}")


def main() -> None:
    successful_command()
    failing_command()
    shell_true_warning()


if __name__ == "__main__":
    main()
