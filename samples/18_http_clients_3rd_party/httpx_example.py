"""`httpx` で HTTP リクエストを送るサンプル（sync + async）。

`httpx` は 2026 年時点で **新規プロジェクトの第一候補** とよく挙がるライブラリ。
- requests に近い API で書ける（移行コストが低い）
- **sync と async の両方を同じ書き味で扱える**
- HTTP/2 オプション対応
- FastAPI の TestClient のバックエンドとして採用されたことで一気に普及

ここでは sync 版と async 版を順番に動かす。
"""

import asyncio

import httpx


GET_URL = "https://api.github.com/zen"
JSON_URL = "https://api.github.com/repos/python/cpython"
POST_URL = "https://httpbin.org/post"
TIMEOUT_SEC = 5.0


def sync_part() -> None:
    """sync API。requests とほぼ同じ書き味。"""
    print("  -- sync --")

    # httpx.get / .post はワンショット用ヘルパ。
    # 本格的に使うときは httpx.Client（後述）を使い回すのが定番。
    resp = httpx.get(GET_URL, timeout=TIMEOUT_SEC)
    resp.raise_for_status()
    print(f"  GET text  : status={resp.status_code}, body={resp.text!r}")

    # params= / headers= / .json() の挙動は requests と同じ。
    resp = httpx.get(
        JSON_URL,
        params={"foo": "bar"},
        headers={"Accept": "application/vnd.github+json", "User-Agent": "python-sample-box/0.1"},
        timeout=TIMEOUT_SEC,
    )
    resp.raise_for_status()
    data = resp.json()
    print(f"  GET json  : full_name={data['full_name']}, stars={data['stargazers_count']}")

    # httpx.Client は requests.Session 相当。
    # コネクション再利用 + 共通設定。HTTP/2 を有効化したい場合は Client(http2=True)。
    with httpx.Client(
        headers={"User-Agent": "python-sample-box/0.1"},
        timeout=TIMEOUT_SEC,
    ) as client:
        try:
            resp = client.post(POST_URL, json={"name": "alice", "score": 82})
            resp.raise_for_status()
            print(f"  POST json : status={resp.status_code}, echoed={resp.json().get('json')}")
        except httpx.HTTPError as exc:
            print(f"  POST json : skipped ({exc})")


async def async_part() -> None:
    """async API。AsyncClient を使う以外は sync 版とほぼ同じ。"""
    print("  -- async --")

    # AsyncClient は Client の async 版。with 文も async with になる。
    # httpx の最大の差別化要因がここ。requests には async 版が存在しない。
    async with httpx.AsyncClient(timeout=TIMEOUT_SEC) as client:
        # 並行に 2 本叩いて待つ、というのが async の素の使い方。
        # asyncio.gather で並行実行した GET の結果をまとめて受け取る。
        try:
            r1, r2 = await asyncio.gather(
                client.get(GET_URL),
                client.get(GET_URL),
            )
            print(f"  GET x2    : statuses=({r1.status_code}, {r2.status_code})")
        except httpx.HTTPError as exc:
            print(f"  GET x2    : skipped ({exc})")

        # async でも書き味は sync と一致する。await が付くだけ。
        try:
            resp = await client.post(POST_URL, json={"name": "bob", "score": 70})
            resp.raise_for_status()
            print(f"  POST json : status={resp.status_code}, echoed={resp.json().get('json')}")
        except httpx.HTTPError as exc:
            print(f"  POST json : skipped ({exc})")


def main() -> None:
    # 例外階層は httpx.HTTPError が頂点（requests の RequestException 相当）。
    sync_part()
    asyncio.run(async_part())


if __name__ == "__main__":
    main()
