"""`collections` 実用編: dict / list だけではない標準コンテナ。

業務コードでは、素の dict / list よりも意図が伝わる collection を使うと
コードが短く、バグも入りにくくなることがある。
"""

from collections import ChainMap, Counter, defaultdict, deque, namedtuple


def counter_example() -> None:
    print("--- Counter: 件数集計 ---")
    words = ["error", "info", "error", "warning", "info", "error"]
    counts = Counter(words)
    print(counts)
    print(f"最頻値: {counts.most_common(1)}")


def defaultdict_example() -> None:
    print("\n--- defaultdict: group by ---")
    users = [("tokyo", "alice"), ("osaka", "bob"), ("tokyo", "carol")]
    by_city: defaultdict[str, list[str]] = defaultdict(list)
    for city, name in users:
        # if city not in by_city: by_city[city] = [] を書かずに済む。
        by_city[city].append(name)
    print(dict(by_city))


def deque_example() -> None:
    print("\n--- deque: queue / 固定長履歴 ---")
    queue: deque[str] = deque()
    queue.append("job-1")
    queue.append("job-2")
    print(f"pop left: {queue.popleft()}")

    recent: deque[str] = deque(maxlen=3)
    for event in ["open", "click", "scroll", "close"]:
        recent.append(event)
    print(f"直近3件: {list(recent)}")


def chainmap_example() -> None:
    print("\n--- ChainMap: 設定の優先順位 ---")
    defaults = {"timeout": "30", "debug": "false"}
    file_config = {"timeout": "10"}
    env_config = {"debug": "true"}
    # ChainMap は左から順に key を探す「先勝ち」の view。
    # ここでは env_config -> file_config -> defaults の順に優先される。
    # dict をマージして新しい dict を作るわけではない点に注意。
    # config["x"] = ... のように代入すると、一番左の env_config に書き込まれる。
    config = ChainMap(env_config, file_config, defaults)
    print(f"timeout={config['timeout']}, debug={config['debug']}")


def namedtuple_example() -> None:
    print("\n--- namedtuple: 軽量な名前付き tuple ---")
    # Point = namedtuple(...) は「型」を作る
    # point = Point(...) は「値」を作る
    # 値を return すれば、呼び出し元でも point.x で読める
    # ただし Point という型名を呼び出し元で使いたいなら、型定義も外側に置く必要がある
    Point = namedtuple("Point", ["x", "y"])
    point = Point(10, 20)
    print(f"x={point.x}, y={point.y}, tupleとしても使える={point[0]}")


def main() -> None:
    counter_example()
    defaultdict_example()
    deque_example()
    chainmap_example()
    namedtuple_example()


if __name__ == "__main__":
    main()
