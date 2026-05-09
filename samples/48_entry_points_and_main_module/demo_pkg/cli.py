"""console script から呼ばれる関数を置く想定のモジュール。"""

from demo_pkg import APP_NAME


def main(source: str = "console script") -> None:
    print(f"{APP_NAME}.cli.main() is {source}")
