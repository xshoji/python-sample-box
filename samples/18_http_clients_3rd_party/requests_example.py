"""`requests` で HTTP リクエストを送るサンプル。

`requests` は Python の HTTP クライアントとして長年デファクトだった存在。
sync 専用・HTTP/1.1 専用・maintenance mode という制約はあるが、API の素直さと
資料の多さで既存プロジェクトでは依然として広く使われている。
"""

import requests


GET_URL = "https://api.github.com/zen"
JSON_URL = "https://api.github.com/repos/python/cpython"
POST_URL = "https://httpbin.org/post"
TIMEOUT_SEC = 5.0


def main() -> None:
    # 1. 単純な GET。.text で本文、.status_code でステータス。
    resp = requests.get(GET_URL, timeout=TIMEOUT_SEC)
    resp.raise_for_status()  # 4xx/5xx を例外にする定番イディオム
    print(f"  GET text  : status={resp.status_code}, body={resp.text!r}")

    # 2. params= に dict を渡せばクエリ文字列を組み立ててくれる。
    #    headers= でカスタムヘッダ、.json() で JSON パース。
    resp = requests.get(
        JSON_URL,
        params={"foo": "bar"},
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "python-sample-box/0.1",
        },
        timeout=TIMEOUT_SEC,
    )
    resp.raise_for_status()
    data = resp.json()
    print(f"  GET json  : full_name={data['full_name']}, stars={data['stargazers_count']}")

    # 3. POST は json= に dict を渡すだけ。
    #    自動で json.dumps + Content-Type: application/json が付く。
    try:
        resp = requests.post(POST_URL, json={"name": "alice", "score": 82}, timeout=TIMEOUT_SEC)
        resp.raise_for_status()
        echoed = resp.json().get("json")
        print(f"  POST json : status={resp.status_code}, echoed={echoed}")
    except requests.RequestException as exc:
        # requests のネットワーク・HTTP 系例外は RequestException が頂点。
        print(f"  POST json : skipped ({exc})")

    # 4. Session = TCP コネクション再利用 + 共通ヘッダ管理。
    #    現場の API クライアントはほぼ Session を 1 つ使い回す形になる。
    with requests.Session() as session:
        session.headers.update({"User-Agent": "python-sample-box/0.1"})
        try:
            r1 = session.get(GET_URL, timeout=TIMEOUT_SEC)
            r2 = session.get(GET_URL, timeout=TIMEOUT_SEC)
            print(f"  Session   : statuses=({r1.status_code}, {r2.status_code})")
        except requests.RequestException as exc:
            print(f"  Session   : skipped ({exc})")


if __name__ == "__main__":
    main()
