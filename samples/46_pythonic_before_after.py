"""Pythonic な書き換えのビフォーアフター集。

Python では「動く」だけでなく、標準的なイディオムを使うと意図が伝わりやすい。
他言語の癖で書きがちな処理を、Python らしい形に置き換える例をまとめる。
"""

from collections import Counter


def main() -> None:
    names = ["alice", "bob", "carol"]
    scores = [80, 95, 72]

    print("--- 1. index で回すより enumerate ---")
    for index, name in enumerate(names, start=1):
        print(f"{index}: {name}")

    print("\n--- 2. 2 つのリストを並行して見るなら zip ---")
    for name, score in zip(names, scores):
        print(f"{name}: {score}")

    print("\n--- 3. 空判定は len(...) == 0 より truthiness ---")
    tasks: list[str] = []
    if not tasks:
        print("タスクは空です")

    print("\n--- 4. list を作るだけなら append ループより内包表記 ---")
    passed_names = [name for name, score in zip(names, scores) if score >= 80]
    print(passed_names)

    print("\n--- 5. 手動集計より Counter ---")
    words = ["python", "java", "python", "go", "python", "go"]
    print(Counter(words))

    print("\n--- 6. None 判定は == ではなく is ---")
    value: str | None = None
    if value is None:
        print("value は None")

    print("\n--- 7. dict の存在確認と取得は get が便利 ---")
    user = {"name": "alice"}
    print(user.get("email", "メール未登録"))


if __name__ == "__main__":
    main()
