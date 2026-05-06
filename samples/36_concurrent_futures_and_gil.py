"""`concurrent.futures` と GIL: ThreadPool / ProcessPool の使い分け。

Python の CPython 実装には GIL (Global Interpreter Lock) があるため、
CPU を使い切る純粋な Python 処理は複数スレッドにしても速くなりにくい。

- I/O 待ちが中心: `ThreadPoolExecutor`
- CPU 計算が中心 : `ProcessPoolExecutor`
"""

import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def fake_io(name: str) -> str:
    time.sleep(0.2)
    return f"done:{name}"


def cpu_work(n: int) -> int:
    # 小さめの CPU 処理。ProcessPool は関数が top-level にある必要がある。
    total = 0
    for i in range(n):
        total += i * i
    return total


def thread_pool_example() -> None:
    print("--- ThreadPoolExecutor: I/O 待ち向き ---")
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fake_io, ["A", "B", "C"]))
    print(results)
    print(f"elapsed={time.perf_counter() - start:.2f}s（直列なら約0.6秒）")


def process_pool_example() -> None:
    print("\n--- ProcessPoolExecutor: CPU 処理向き ---")
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(cpu_work, [200_000, 250_000]))
    print([str(result)[:8] + "..." for result in results])


def main() -> None:
    thread_pool_example()
    process_pool_example()


if __name__ == "__main__":
    main()
