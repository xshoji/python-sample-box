"""`asyncio` の最小サンプル: `async` / `await` / `gather`。

asyncio は **協調的（cooperative）マルチタスク** を提供する標準ライブラリ。
スレッドではなく単一スレッド上で「I/O 待ちの間に別タスクへ譲る」ことで並行実行する。

押さえるポイント:

- `async def` で定義された関数を呼ぶと、**実行されずに coroutine オブジェクトが返る**
- 実際に走らせるには `await` するか、`asyncio.run()` の中に渡す
- 複数の coroutine を **並行に** 実行したいときは `asyncio.gather(...)` を使う
- スレッドではないので、`time.sleep()` を使うとイベントループ全体が止まる
  → 待機は `await asyncio.sleep(...)` を使う

他言語との対比:

- JavaScript: `async`/`await` の挙動はほぼ同じ。`Promise.all` ≒ `asyncio.gather`
- Java      : CompletableFuture / Project Loom 系（Virtual Thread）に近い概念
- Go        : goroutine と違い、Python の async は単一スレッド・明示的な `await` が必要
"""

import asyncio
import time


# `async def` で定義された関数は coroutine function。
# 呼ぶだけでは中身は実行されず、coroutine オブジェクトが返るだけ。
async def fetch(name: str, seconds: float) -> str:
    print(f"  [{time.perf_counter() - START:.2f}s] start  {name}")
    # I/O 待ちの代わり。本物の I/O（HTTP, DB）も await で同様に書ける。
    await asyncio.sleep(seconds)
    print(f"  [{time.perf_counter() - START:.2f}s] done   {name}")
    return f"result-of-{name}"


async def run_sequentially() -> list[str]:
    # await を順番に書くと、前の完了を待ってから次が走る = 直列。
    a = await fetch("A", 1.0)
    b = await fetch("B", 1.0)
    return [a, b]


async def run_concurrently() -> list[str]:
    # gather は coroutine を複数渡すと、まとめて並行実行して結果のリストを返す。
    # I/O 待ちが重なる場合、合計時間が「最も長いタスク」分まで縮む。
    return await asyncio.gather(
        fetch("X", 1.0),
        fetch("Y", 1.0),
        fetch("Z", 1.0),
    )


START = 0.0  # main の中で計測開始時刻を入れる


async def amain() -> None:
    global START

    print("--- 直列実行 (await を順に並べた場合) ---")
    START = time.perf_counter()
    results = await run_sequentially()
    print(f"  results = {results}")
    print(f"  elapsed = {time.perf_counter() - START:.2f}s  (直列なので合計は ≒ 2.0s)")

    print("\n--- 並行実行 (asyncio.gather) ---")
    START = time.perf_counter()
    results = await run_concurrently()
    print(f"  results = {results}")
    print(f"  elapsed = {time.perf_counter() - START:.2f}s  (並行なので最長 ≒ 1.0s)")

    # ============================================================
    # コルーチンを await し忘れる罠
    # ============================================================
    # async 関数を「呼ぶだけ」だと、実行されない coroutine オブジェクトが返るだけ。
    # 多くの場合 RuntimeWarning: coroutine '...' was never awaited が出る。
    print("\n--- await し忘れに注意 ---")
    coro = fetch("forgotten", 0.0)  # まだ実行されていない
    print(f"  type = {type(coro).__name__}  (この時点では未実行)")
    # ちゃんと実行する
    print(f"  await した結果: {await coro}")


def main() -> None:
    # `asyncio.run` がイベントループを作り、coroutine を最後まで走らせて閉じる。
    # アプリのエントリポイントで 1 回だけ呼ぶのが基本。
    asyncio.run(amain())


if __name__ == "__main__":
    main()
