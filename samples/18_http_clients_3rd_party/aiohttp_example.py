"""`aiohttp` で HTTP リクエストを送るサンプル（async 専用）。

`aiohttp` は async-first の HTTP ライブラリ。クライアントだけでなく **HTTP サーバ** も
同梱しているのが特徴で、async サーバ実装と組み合わせて使うことが多い。

クライアント単体としての書き味は httpx の方が requests に近くて新規には書きやすいが、
- 大量並行・クローラ系
- 既に aiohttp で組んだ async ワークロードに合わせたい
というケースでは aiohttp が現役で選ばれる。
"""

import asyncio

import aiohttp


GET_URL = "https://api.github.com/zen"
JSON_URL = "https://api.github.com/repos/python/cpython"
POST_URL = "https://httpbin.org/post"
TIMEOUT_SEC = 5.0


async def run() -> None:
    # aiohttp は ClientSession を作って使い回すのが基本（毎回作ると非効率）。
    # timeout は ClientTimeout オブジェクトで設定する点が requests / httpx と違う。
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SEC)
    headers = {"User-Agent": "python-sample-box/0.1"}

    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        # 1. 単純な GET。
        #    レスポンスも async with で受ける必要がある（接続を確実に解放するため）。
        #    .text() / .json() は coroutine なので await を付けて呼ぶ。
        try:
            async with session.get(GET_URL) as resp:
                resp.raise_for_status()
                body = await resp.text()
                print(f"  GET text  : status={resp.status}, body={body!r}")
        except aiohttp.ClientError as exc:
            print(f"  GET text  : skipped ({exc})")

        # 2. params + Accept ヘッダ + JSON パース。
        try:
            async with session.get(
                JSON_URL,
                params={"foo": "bar"},
                headers={"Accept": "application/vnd.github+json"},
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                print(
                    f"  GET json  : full_name={data['full_name']}, stars={data['stargazers_count']}"
                )
        except aiohttp.ClientError as exc:
            print(f"  GET json  : skipped ({exc})")

        # 3. POST JSON。json= に dict を渡すだけ（requests / httpx と同じ）。
        try:
            async with session.post(POST_URL, json={"name": "carol", "score": 91}) as resp:
                resp.raise_for_status()
                data = await resp.json()
                print(f"  POST json : status={resp.status}, echoed={data.get('json')}")
        except aiohttp.ClientError as exc:
            print(f"  POST json : skipped ({exc})")

        # 4. 並行 GET。asyncio.gather にぶら下げるのは aiohttp 流の典型パターン。
        async def fetch_status(url: str) -> int:
            async with session.get(url) as r:
                return r.status

        try:
            statuses = await asyncio.gather(fetch_status(GET_URL), fetch_status(GET_URL))
            print(f"  GET x2    : statuses={tuple(statuses)}")
        except aiohttp.ClientError as exc:
            print(f"  GET x2    : skipped ({exc})")


def main() -> None:
    # aiohttp は同期 API を提供しないため、必ず asyncio.run でエントリする。
    # 例外階層は aiohttp.ClientError が頂点。
    asyncio.run(run())


if __name__ == "__main__":
    main()
