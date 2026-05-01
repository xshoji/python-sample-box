"""`if __name__ == "__main__"` と import 時の実行。

Python ファイルは「スクリプト」として実行もでき、「モジュール」として import もできます。
トップレベルに書いた処理は import 時にも実行されるため、副作用を避けたい処理は
main guard の中に置くのが定番です。
"""

import supporting_module_for_import


def main() -> None:
    print("03_main_guard_and_imports.py was executed as a script")
    print(supporting_module_for_import.greet("alice"))


if __name__ == "__main__":
    main()
