"""3rd party の `requests` で HTTP リクエストを送るサンプル。

`requests` は Python で HTTP を扱うときの事実上の標準ライブラリ。
標準の urllib より API が読みやすく、JSON・タイムアウト・セッションなどの
日常的な操作がそのまま書ける。

このサンプルは **このディレクトリ配下に閉じた `pyproject.toml` + `uv` で動かす** 構成にしてある。
正規の動かし方:

    cd samples/18_http_request_with_requests
    uv sync          # .venv をこの dir に作って requests を入れる
    uv run main.py   # その .venv の Python で実行

`scripts/run_all.py` からはこのサンプルを除外している（EXCLUDED リスト参照）。
詳しくは同ディレクトリの README.md を参照。
"""

from __future__ import annotations

import sys


# ------------------------------------------------------------------
# 前提: requests が入っていないときは何もせずに正常終了する。
# 直接 `python main.py` で叩かれた場合の事故防止用。
# 正規の動かし方は uv sync → uv run main.py。
# ------------------------------------------------------------------
try:
    import requests
except ModuleNotFoundError:
    print("requests is not installed.")
    print("  setup: cd samples/18_http_request_with_requests && uv sync")
    print("  run  : uv run main.py")
    sys.exit(0)


GET_URL = "https://api.github.com/zen"
JSON_URL = "https://api.github.com/repos/python/cpython"
POST_URL = "https://httpbin.org/post"
TIMEOUT_SEC = 5.0


def get_text() -> None:
    """1. 単純な GET。レスポンス本文は .text で取れる。"""
    print("# 1. GET text")
    # requests.get は urllib より一段階シンプル。
    # timeout は必須レベル（指定しないと「永久に待つ」可能性がある）。
    resp = requests.get(GET_URL, timeout=TIMEOUT_SEC)
    resp.raise_for_status()  # 4xx / 5xx を HTTPError として投げる。urllib でいう HTTPError 相当
    print(f"  status={resp.status_code}")
    print(f"  body={resp.text!r}")


def get_json() -> None:
    """2. GET + JSON パース + ヘッダ + クエリパラメータ"""
    print("# 2. GET json with headers and params")
    resp = requests.get(
        JSON_URL,
        # params は dict を渡すだけで自動的に ?key=value に組み立ててくれる。
        # urllib では urllib.parse.urlencode を自分で呼ぶ必要があった。
        params={"foo": "bar"},
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "python-sample-box/0.1",
        },
        timeout=TIMEOUT_SEC,
    )
    resp.raise_for_status()
    # .json() は内部で json.loads を呼んでくれる。dict / list が返る。
    data = resp.json()
    print(f"  status={resp.status_code}")
    print(f"  full_name={data['full_name']}, stars={data['stargazers_count']}")


def post_json() -> None:
    """3. POST で JSON を送る — `json=` キーワードが便利。"""
    print("# 3. POST json body")
    payload = {"name": "alice", "score": 82}
    try:
        # json= に dict を渡すと:
        #   - 自動的に json.dumps される
        #   - Content-Type: application/json が自動で付く
        # urllib では自分でやっていた処理がワンライナーになる。
        resp = requests.post(POST_URL, json=payload, timeout=TIMEOUT_SEC)
        resp.raise_for_status()
        data = resp.json()
        print(f"  status={resp.status_code}, echoed_json={data.get('json')}")
    except requests.RequestException as exc:
        # requests のネットワーク・HTTP 系例外はすべて RequestException を継承している。
        # 「ネットワーク絡みなら何でもキャッチしたい」ときはこれを使う。
        print(f"  POST skipped (network error): {exc}")


def use_session() -> None:
    """4. Session — 同じホストに複数回叩くときの定番。

    Session を使うと:
      - 内部で TCP コネクションを使い回す（毎回 connect しなくて済む）
      - 共通ヘッダ（API キーや User-Agent）を 1 か所で管理できる
      - cookie が自動で引き継がれる

    現場の API クライアントはほぼ Session を 1 つ作って使い回す形になる。
    """
    print("# 4. Session reuse")
    with requests.Session() as session:
        # ここで設定したヘッダは、この session 経由のリクエストすべてに付く。
        session.headers.update({"User-Agent": "python-sample-box/0.1"})
        try:
            resp1 = session.get(GET_URL, timeout=TIMEOUT_SEC)
            resp2 = session.get(GET_URL, timeout=TIMEOUT_SEC)
            print(f"  resp1.status={resp1.status_code}, resp2.status={resp2.status_code}")
        except requests.RequestException as exc:
            print(f"  session GET skipped (network error): {exc}")


def main() -> None:
    # urllib との比較で覚えておくとよい点:
    #   - resp.text / resp.json() で本文を直接扱える（自分で decode しなくていい）
    #   - timeout は必ず指定する（指定しないと無限待機の可能性）
    #   - 例外階層は requests.RequestException を頂点にした 1 つの木にまとまっている
    #     （HTTPError / ConnectionError / Timeout などはすべてサブクラス）
    try:
        get_text()
        get_json()
        post_json()
        use_session()
    except requests.HTTPError as exc:
        print(f"HTTP error: {exc}")
    except requests.RequestException as exc:
        print(f"network error: {exc}")


if __name__ == "__main__":
    main()
