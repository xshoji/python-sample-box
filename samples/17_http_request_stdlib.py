"""標準ライブラリだけで HTTP リクエストを送る (urllib.request)。

Python は **3rd party 不要で HTTP が叩ける** のが特徴の 1 つ。
標準ライブラリの ``urllib.request`` でだいたい何でもできる。
ただし API が低レベルで読みにくいので、現場では requests / httpx を使うことが多い
（次サンプル 18_http_request_with_requests/ を参照）。

ここでは urllib の代表的な使い方を 4 つ示す。

ネットワーク不通や公開 API 側の障害で例外になる可能性があるため、
失敗時はメッセージを出して exit 0 で終わる（``run_all.py`` を壊さないため）。
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request


# httpbin / GitHub API は HTTP の例として広く使われる公開エンドポイント。
GET_URL = "https://api.github.com/zen"           # 1 行のテキストを返す
JSON_URL = "https://api.github.com/repos/python/cpython"
POST_URL = "https://httpbin.org/post"             # 送ったデータをそのまま返してくれる
TIMEOUT_SEC = 5.0


def get_text() -> None:
    """1. 単純な GET（レスポンスボディを文字列で取得）"""
    print("# 1. GET text")
    # urlopen は context manager として使うのが定番。with を抜けると close される。
    with urllib.request.urlopen(GET_URL, timeout=TIMEOUT_SEC) as resp:
        # resp.status は HTTP ステータスコード、resp.read() は bytes を返す。
        # 文字コードはサーバが Content-Type で返す charset を見て decode するのが厳密だが、
        # API 系は UTF-8 がほとんどなので、学習用には固定で OK。
        body = resp.read().decode("utf-8")
        print(f"  status={resp.status}")
        print(f"  body={body!r}")


def get_json() -> None:
    """2. GET + JSON パース + リクエストヘッダ追加"""
    print("# 2. GET json with custom headers")
    # User-Agent や Accept を付けたいときは Request オブジェクトを作る。
    # urlopen に直接 URL 文字列を渡す書き方ではヘッダを付けられない。
    req = urllib.request.Request(
        JSON_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "python-sample-box/0.1",  # GitHub API は UA 必須
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
        # JSON は bytes → str → json.loads で dict / list に変換する。
        data = json.loads(resp.read().decode("utf-8"))
        print(f"  status={resp.status}")
        print(f"  full_name={data['full_name']}, stars={data['stargazers_count']}")


def post_json() -> None:
    """3. POST で JSON ボディを送る"""
    print("# 3. POST json body")
    payload = {"name": "alice", "score": 82}
    # JSON を送るときは、自分で json.dumps → bytes にエンコードして data に渡す。
    # data を渡した時点で urllib は自動的に POST になる。
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        POST_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",  # 明示しておくと読みやすい
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # httpbin は受け取った JSON を data フィールドに echo back する。
            print(f"  status={resp.status}, echoed_json={data.get('json')}")
    except urllib.error.URLError as exc:
        # httpbin.org は時々落ちる。学習用には致命傷ではないので握って終わる。
        print(f"  POST skipped (network error): {exc}")


def post_form() -> None:
    """4. POST で form-urlencoded を送る（HTML フォーム送信と同じ形式）"""
    print("# 4. POST form-urlencoded")
    # urllib.parse.urlencode は dict を "key=value&..." 形式の str にする。
    # bytes に encode して data に渡すと Content-Type は自動で
    # application/x-www-form-urlencoded になる。
    form = urllib.parse.urlencode({"q": "python tuple", "page": 1}).encode("utf-8")
    req = urllib.request.Request(POST_URL, data=form, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"  status={resp.status}, echoed_form={data.get('form')}")
    except urllib.error.URLError as exc:
        print(f"  POST skipped (network error): {exc}")


def main() -> None:
    # ====================================================================
    # 例外の階層（覚えておくと役立つ）
    # ====================================================================
    # urllib.error.URLError    : ネットワーク全般の失敗（DNS、接続不能、timeout 等）
    # urllib.error.HTTPError   : URLError のサブクラス。4xx / 5xx を例外として投げる
    #
    # → 「4xx/5xx だけ拾いたい」なら HTTPError、
    #   「とにかくネットワーク絡みの失敗」を拾いたいなら URLError をキャッチする。
    try:
        get_text()
        get_json()
        post_json()
        post_form()
    except urllib.error.HTTPError as exc:
        # 4xx / 5xx。レスポンスボディも resp.read() で読める。
        print(f"HTTP error: {exc.code} {exc.reason}")
    except urllib.error.URLError as exc:
        # 接続失敗、DNS 解決失敗、timeout など。
        print(f"network error: {exc}")


if __name__ == "__main__":
    main()
