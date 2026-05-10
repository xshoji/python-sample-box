"""plugin / registry パターン: decorator で handler を登録する。

Python では decorator と dict を使って、コマンド名やイベント名に対応する関数を登録する
registry パターンをよく書く。Flask の route decorator や CLI の subcommand にも近い発想。
"""

from collections.abc import Callable


type Handler = Callable[[list[str]], str]

REGISTRY: dict[str, Handler] = {}


def command(name: str) -> Callable[[Handler], Handler]:
    def decorator(func: Handler) -> Handler:
        REGISTRY[name] = func
        return func

    return decorator


@command("hello")
def hello(args: list[str]) -> str:
    name = args[0] if args else "guest"
    return f"hello, {name}"


@command("add")
def add(args: list[str]) -> str:
    numbers = [int(value) for value in args]
    return str(sum(numbers))


def dispatch(line: str) -> str:
    parts = line.split()
    if not parts:
        raise ValueError("空のコマンドです")

    name, *args = parts
    try:
        handler = REGISTRY[name]
    except KeyError as error:
        raise ValueError(f"未知のコマンドです: {name}") from error
    return handler(args)


def main() -> None:
    print("--- 登録済み command ---")
    print(sorted(REGISTRY))

    print("\n--- dispatch ---")
    for line in ["hello alice", "add 10 20 30"]:
        print(f"{line!r} -> {dispatch(line)!r}")

    print("\n新しい handler は @command('name') を付けた関数を追加するだけで登録できる")


if __name__ == "__main__":
    main()
