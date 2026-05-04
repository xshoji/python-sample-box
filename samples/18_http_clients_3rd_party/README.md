# 18_http_clients_3rd_party

Python の **3rd party HTTP クライアント** の主要どころを 1 か所に集めて比較するサンプル集です。`samples/17_http_request_stdlib.py`（標準ライブラリ `urllib.request` 版）と並べて読むと、なぜわざわざ外部ライブラリを入れるのかが分かります。

このディレクトリは独立した uv プロジェクトになっており、依存パッケージはここの `.venv/` にだけ入ります。リポジトリ全体（stdlib のみ方針）には影響しません。

## 含まれるサンプル

| ファイル | 採用ライブラリ | sync | async | HTTP/2 | 主な位置付け |
| --- | --- | :-: | :-: | :-: | --- |
| [`requests_example.py`](./requests_example.py) | [`requests`](https://requests.readthedocs.io/) | ✓ | ✗ | ✗ | 長年のデファクト。資料・既存コードが圧倒的。maintenance mode |
| [`httpx_example.py`](./httpx_example.py) | [`httpx`](https://www.python-httpx.org/) | ✓ | ✓ | ✓ (オプション) | 2026 年の **新規プロジェクト第一候補**。requests に近い API + async |
| [`aiohttp_example.py`](./aiohttp_example.py) | [`aiohttp`](https://docs.aiohttp.org/) | ✗ | ✓ | ✗ | async 専用。クライアント + **サーバ** も同梱。並行クローラの定番 |

`main.py` はこの 3 つを順に呼ぶオーケストレータです。

## 動かし方

[uv](https://docs.astral.sh/uv/) が入っている前提です（無ければ `samples/15_python_versions_and_managers/` 参照）。

```bash
cd samples/18_http_clients_3rd_party

uv sync          # .venv をこの dir に作って requests / httpx / aiohttp を入れる
uv run main.py   # 3 つすべて順に実行

# 個別に動かしたい場合:
uv run requests_example.py
uv run httpx_example.py
uv run aiohttp_example.py
```

`uv sync` で作られる `.venv/` と `uv.lock` はこの dir に閉じています。`scripts/run_all.py` の一括実行対象からは `EXCLUDED` で除外しています。

## 2026 年時点の選び方の指針

ざっくりとした実務感覚です。

- **新規プロジェクトを始める** → `httpx`
  - sync で書き始めて、必要になったら同じ API で async に移行できる
  - HTTP/2 が必要なら `httpx.Client(http2=True)`（要 `httpx[http2]`）
- **既存コードが requests を使っている / 既存資料に従いたい** → `requests` のまま
  - 移行コストを払うほどの差はない場面が多い。sync で十分なら現役
- **async が前提のワークロード（クローラ・大量並行・aiohttp サーバと共存）** → `aiohttp` か `httpx`
  - aiohttp サーバとセットなら `aiohttp.ClientSession`、それ以外は httpx の方が書きやすい
- **超低レベル制御が要る（SDK 実装、独自プール、リトライ細部）** → `urllib3` を直接
  - これは「ライブラリ実装者用」の選択肢。次節参照

### `requests` は終わったのか？

「終わった」と言うのは強すぎますが、**新機能はもう載らない** と思って良いステータスです。

- HTTP/2 / HTTP/3 サポートは入らない
- async サポートも入らない
- bugfix と security 対応は継続

そのため新規採用は減り、既存プロジェクトでの利用が惰性で続いている、という構図です。`niquests`（requests 互換 + HTTP/2/3 + async）や `urllib3-future` といった「requests / urllib3 の延命派生」も登場していますが、まだ実務採用は少数派で、多数派は `httpx` に流れています。

## OpenAPI Generator が `requests` を採用していない理由

[OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator) の Python クライアントでは、`library` オプションで HTTP 層を切り替えられますが、選べるのは

```
urllib3（既定） / asyncio / tornado（deprecated） / httpx
```

の 4 つで、**`requests` は最初から入っていません**。これは Python の HTTP 事情を反映したいくつかの構造的な理由があります。

### 1. requests 自体が urllib3 のラッパー

`requests` の HTTP コア層はまるごと `urllib3` です。つまり生成 SDK が `urllib3` を直接使えば、

- `requests` + `charset-normalizer` + `idna` + `certifi` という **4 つの依存を経由する分の薄い皮** を SDK 利用者に強制しない
- 機能的には `urllib3` だけで全部できる

ので、`requests` 版を別ジェネレーターとして用意しても **urllib3 版の機能制限サブセットになるだけ** で得がありません。

### 2. SDK の依存は最小化したい

生成物は **ライブラリとして配布される** 前提です。アプリと違って利用者の依存ツリーに直接乗ります。`requests` を強制すると、利用側が既に `httpx` だけで統一しているプロジェクトと衝突する余地が増えます。`urllib3` は誰でも入れて構わない最小公約数になりやすい。

### 3. async / HTTP/2 への道がない

`requests` は sync 専用 + HTTP/1.1 専用 + maintenance mode です。新規にジェネレーターのテンプレートを書いてメンテし続ける投資としてリターンが薄く、async が必要なら `asyncio` / `aiohttp` または `httpx` を選ぶ方が将来性があります。実際 OpenAPI Generator は後発で **`httpx` の library 値を追加** しています。

### 4. 低レベル制御の必要性

SDK 生成では以下が頻繁に必要で、これらは `urllib3` の方が素直に書けます。

- `Retry` オブジェクトでの細かい再試行制御（バックオフ、idempotent メソッド限定など）
- `PoolManager` のプール調整、TLS / proxy / SOCKS 設定
- multipart upload の生バイト操作、ストリーミング応答（`preload_content=False`）
- ヘッダ・ボディ差し込みの中間層（middleware 風）

`requests` は一段階抽象化された API のため、テンプレートで生成するコードとしては **隠蔽が逆に邪魔** になりやすいのです。

### 5. 受益層の分散と httpx への合流

「ヒューマンフレンドリーな高レベル API の SDK が欲しい」という需要は、別系統のジェネレーター — [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client) や Speakeasy など — がすでに **`httpx` を採用** して受け止めています。OpenAPI Generator も `httpx` を追加した流れに乗っており、**新規に `requests` 専用ジェネレーターを作る需要そのものが消えている** 状態です。

### まとめ

- 技術的: `requests` を採用しても **urllib3 を間接化するだけ** で利点がない
- 戦略的: sync 専用 + maintenance mode の `requests` に新規投資する価値が薄い
- 進化的: async / HTTP/2 を見据えるなら `httpx` の方が筋が良く、実際そちらが追加された

という三段の理由で、`requests` ベースのコード生成クラスは **作る合理性がない** と判断されていると考えるのが妥当です。

## 注意

- どのライブラリでも `timeout` は **必ず指定** する（無指定だと無期限待機の可能性）。
- ここで叩いている `https://api.github.com/...` や `https://httpbin.org/...` は外部の公開サービスのため、落ちていることもあります。各サンプルは例外を握ってメッセージだけ出して続行する作りです。
