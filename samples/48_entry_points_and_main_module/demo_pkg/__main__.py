"""`python -m demo_pkg` で実行される入口。"""

from demo_pkg.cli import main


main("called from demo_pkg.__main__")
