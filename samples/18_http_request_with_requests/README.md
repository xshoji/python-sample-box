# 18_http_request_with_requests

3rd party の [`requests`](https://requests.readthedocs.io/) で HTTP リクエストを送るサンプルです。前のサンプル `17_http_request_stdlib.py`（標準ライブラリ `urllib.request` 版）と読み比べると、`requests` がどこを楽にしているかが分かります。

## なぜ `requests` を使うのか

Python で HTTP を叩くとき、現場では `requests` か後発の `httpx` が選ばれることがほとんどです。標準ライブラリの `urllib.request` でも同じことはできますが、

- `Request` オブジェクトを毎回作らなくてよい
- `params=` に dict を渡せばクエリ文字列を自動で組み立ててくれる
- `json=` に dict を渡せば自動で `json.dumps` + `Content-Type: application/json` を付けてくれる
- 4xx / 5xx を `raise_for_status()` 1 行でチェックできる
- `Session` でコネクション再利用と共通ヘッダの管理ができる

など、日常的に書くコードが素直になります。逆に「何も入れたくない／環境を汚したくない」場合は urllib のままで十分です。

`httpx` は requests と似た API を持ちつつ async に対応しているのが強みで、新規プロジェクトでは選択肢に入ります。ここではより歴史が長く資料が多い `requests` を扱います。

## このサンプルの位置付け

このリポジトリは **原則 stdlib のみ** で動かす方針です。そのためこのサンプルは特別扱いになっています。

- リポジトリのトップに `pyproject.toml` を置かず、**この dir 専用** の `pyproject.toml` をここに置いている
- 依存パッケージ (`requests`) はこの dir 配下に作る `.venv` にだけ入る（システムや他サンプルに影響しない）
- 一括実行 `scripts/run_all.py` の対象から **除外** されている（`EXCLUDED` リスト参照）
- `uv` でパッケージをインストールしたときだけ動くようになっている

つまり「このサンプルだけ動かしたい人が、自分でセットアップして動かす」ための独立コーナーです。

## 動かし方（uv 利用）

[uv](https://docs.astral.sh/uv/) が入っていることが前提です。入っていない場合は `samples/15_python_versions_and_managers/README.md` を参照してインストールしてください。

```bash
# このサンプルの dir に移動
cd samples/18_http_request_with_requests

# pyproject.toml を読んで .venv を作り、requests を入れる
uv sync

# その .venv の Python で main.py を実行
uv run main.py
```

`uv sync` を実行すると、

- このディレクトリ直下に `.venv/` が作られる（`.gitignore` で除外済み）
- `pyproject.toml` の `dependencies` に従って `requests` が入る
- ロックファイル `uv.lock` がこのディレクトリに作られる

`uv run main.py` は、その `.venv` の Python を自動で選んでスクリプトを実行してくれるので、`source .venv/bin/activate` のようなアクティベートは不要です。

## `uv sync` をしていないときの挙動

このサンプルの `main.py` は、`requests` が見つからない場合に

```
requests is not installed.
  setup: cd samples/18_http_request_with_requests && uv sync
  run  : uv run main.py
```

とだけ表示して何もせず正常終了するようになっています。これは:

- 誤って `python samples/18_http_request_with_requests/main.py` のように直接叩いた場合の事故防止
- 後で `scripts/run_all.py` の除外設定を外したくなったときの保険

を兼ねた防御です。**正規の動かし方は `uv sync` → `uv run main.py`** です。

## 扱っているパターン

`main.py` では現場でよく書く 4 パターンを順に動かします。

1. `requests.get(url, timeout=...)` で単純な GET
2. `params=` / `headers=` を渡す GET と `.json()` でのパース
3. `json=` キーワードで JSON ボディを送る POST
4. `requests.Session()` でコネクション再利用 + 共通ヘッダ

例外は `requests.RequestException` を頂点にした 1 本の階層に整理されているので、「ネットワーク絡みなら何でも捕まえたい」ときはこれをキャッチします。`raise_for_status()` で 4xx / 5xx を `HTTPError` として投げる流儀も、現場のコードでよく見かけます。

## 注意

- `timeout` は **必ず指定** すること。省略すると相手サーバが無反応のときに無期限に待つ可能性があります。
- ここで叩いている `https://api.github.com/...` や `https://httpbin.org/...` は外部の公開サービスです。落ちていることもあるため、サンプル内では例外を握ってメッセージだけ出して終わるようにしています。
