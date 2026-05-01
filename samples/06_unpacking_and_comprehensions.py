"""unpacking と内包表記。

Python では「構造をほどく」「小さな変換を式として書く」機能がよく使われます。
過剰に詰め込むと読みにくくなるため、1画面で意味が追える範囲に留めます。
"""


def main() -> None:
    user = (1001, "alice", "admin")
    user_id, name, role = user
    print(f"user_id={user_id}, name={name}, role={role}")

    first, *middle, last = ["red", "green", "blue", "yellow"]
    print(f"first={first}, middle={middle}, last={last}")

    scores = {"alice": 82, "bob": 59, "carol": 91}

    passed_names = [name for name, score in scores.items() if score >= 80]
    print(f"passed_names = {passed_names}")

    labels = {name: ("pass" if score >= 80 else "retry") for name, score in scores.items()}
    print(f"labels = {labels}")

    pairs = [("host", "localhost"), ("port", "8000")]
    config = dict(pairs)
    print(f"config = {config}")


if __name__ == "__main__":
    main()
