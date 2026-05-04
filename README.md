# python-sample-box

Python の理解を深めるためのサンプル実装集です。

Java / Go / Node.js などの経験がある人が、Python らしい書き方・挙動・文化に早く慣れることを目的にしています。変数、関数、クラスのような一般的なプログラミング概念ではなく、Python 固有の「最初につまずきやすいところ」から扱います。

## 方針

- 標準ライブラリだけで動く小さなサンプルにする
- 説明よりも、実行して挙動を確認できるコードを優先する
- 他言語経験者が比較しやすいように、Python 特有の意図や文化をコメントに残す
- 1ファイル1テーマを基本にする
- 解説 README や補助モジュールを伴うテーマは `samples/NN_name/` ディレクトリ形式にし、エントリポイントは `main.py` に固定する

## 実行方法

このリポジトリのサンプルコードは Python 3.12 系（動作確認は 3.12.13）を前提にしています。`python --version` で `Python 3.12.13` が表示される環境を想定しています。

```bash
python --version
# Python 3.12.13

python samples/01_indentation_and_blocks.py
```

まとめて実行する場合は次のコマンドを使えます。

```bash
python scripts/run_all.py
```

## Python バージョンの目安

調査時点: 2026-05。

Python は 3.x 系が主流です。というより、Python 2.7 は 2020 年に EOL になっており、現在の実務では「Python 3 のどの minor version を使うか」が論点になります。

### 公式サポート状況

Python のバージョン表記は `3.12.13` のように `major.minor.micro` です。`3` が major version、`12` が minor version、`13` が bugfix / security fix の micro version です。このリポジトリは `3.12.13` を基準にしています。

| 系列 | 状態 | 公式サポート期限の目安 | コメント |
| --- | --- | --- | --- |
| 3.14 | bugfix | 2030-10 | 2026年時点の最新安定系列。新機能を追いたい場合の候補。 |
| 3.13 | bugfix | 2029-10 | 新しめの現実的な候補。ライブラリ対応も進みつつある。 |
| 3.12 | security | 2028-10 | **このリポジトリの基準。** 現場・学習・コンテナで無難に選びやすい。 |
| 3.11 | security | 2027-10 | まだ広く使われている。既存プロジェクトではよく見る。 |
| 3.10 | security | 2026-10 | 既存環境では残っているが、新規採用は避けたい。 |
| 3.9 | EOL | 2025-10-31 | OS 由来で残っていることはあるが、新規開発では避ける。 |

このリポジトリは Python 3.12 系（動作確認 3.12.13）を基準にしています。3.12 は security fix のみのフェーズに入っていますが、ライブラリ対応・コンテナイメージ・OS パッケージの揃い方が良く、学習・小規模開発の基準として扱いやすい系列です。新機能を追いたい場合は 3.13 / 3.14 を、既存プロジェクトに合わせる場合は 3.10 / 3.11 を選ぶこともあります。

### OS ごとの標準搭載事情

| OS | 標準搭載・既定の傾向 | 開発時の考え方 |
| --- | --- | --- |
| Windows | CPython は OS に標準搭載されていない。`python` コマンドが Microsoft Store や Python install manager へ誘導することはある。 | python.org、Microsoft Store、`winget`、`uv`、`pyenv-win` などで明示的に入れる。 |
| macOS | Python 2.7 は macOS 12.3 以降で削除済み。`/usr/bin/python3` は Xcode Command Line Tools 由来の stub / runtime で、アプリや開発環境が依存すべきものではない。 | Homebrew、python.org installer、`pyenv`、`uv` などでプロジェクト用の Python を用意する。 |
| Linux | ディストリビューションにより異なる。Ubuntu 24.04 LTS は 3.12、Ubuntu 22.04 LTS は 3.10、Debian 12 は 3.11、Debian 13 は 3.13、Fedora 41 は 3.13、RHEL 9 は既定が 3.9 で追加の 3.11 / 3.12 も提供される。 | system Python は OS 管理用でもあるため置き換えない。開発では `venv`、`uv`、`pyenv`、Docker image などで分離する。 |

特に Linux では、`/usr/bin/python3` は apt / dnf などの OS パッケージ管理と結びついています。`sudo pip install ...` や system Python の上書きは避け、プロジェクトごとに仮想環境を作るのが Python の現場では一般的です。

### 現場利用の傾向

実務では「最新をすぐ使う」よりも「1〜2世代前の安定版を使う」傾向があります。JetBrains / PSF の Python Developers Survey 2024 を元にした 2025 年の分析では、Python 3.11 利用者が 48%、3.10 以下が 27%、最新系列を使う人が 15% 程度とされています。また、83% は最新より1年以上古い Python を使っているという分析でした。

このため、2026年時点の肌感としては次のように考えるとよさそうです。

- 学習・新規の小さなプロジェクト: 3.12 または 3.13
- 新機能を追いたいプロジェクト: 3.14。ただし依存ライブラリの対応を確認する
- 既存業務システム: 3.10〜3.12 が残りやすい
- Linux サーバーの OS 標準 Python: ディストリビューションのリリース時期に強く依存する
- コンテナ開発: `python:3.12`、`python:3.13`、`python:3.14` のように明示的に固定しやすい

### 参考情報

- [Python Developer's Guide: Status of Python versions](https://devguide.python.org/versions/)
- [Python.org Downloads](https://www.python.org/downloads/)
- [Python on Windows](https://docs.python.org/3/using/windows.html)
- [Ubuntu: Available Python versions](https://documentation.ubuntu.com/ubuntu-for-developers/reference/availability/python/)
- [Debian Wiki: Python](https://wiki.debian.org/Python)
- [Red Hat Enterprise Linux 9: Installing and using Python](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/installing_and_using_dynamic_programming_languages/assembly_installing-and-using-python_installing-and-using-dynamic-programming-languages)
- [The State of Python 2025: Trends and Survey Insights](https://blog.jetbrains.com/pycharm/2025/08/the-state-of-python-2025/)
- [Docker Official Image: python](https://hub.docker.com/_/python)

## サンプル一覧

| ファイル | テーマ |
| --- | --- |
| `samples/01_indentation_and_blocks.py` | インデントが構文そのものであること、ブロックスコープではないこと |
| `samples/02_dunder_init_and_repr.py` | `__init__` と代表的な dunder method |
| `samples/03_main_guard_and_imports.py` | `if __name__ == "__main__"` と import 時の実行 |
| `samples/04_none_truthiness_identity.py` | `None`、真偽値判定、`is` と `==` の違い |
| `samples/05_mutability_and_default_args.py` | mutable object とデフォルト引数の罠 |
| `samples/06_unpacking_and_comprehensions.py` | unpacking、内包表記、Python らしいデータ変換 |
| `samples/07_iterators_generators.py` | iterable / iterator / generator の考え方 |
| `samples/08_context_managers_with.py` | `with` と context manager |
| `samples/09_decorators.py` | decorator が「関数を受け取り関数を返す」仕組み |
| `samples/10_dataclasses.py` | `dataclass` による値オブジェクト的なクラス |
| `samples/11_type_hints_are_not_runtime_checks.py` | type hints は実行時チェックではないこと |
| `samples/12_eafp_exceptions.py` | Python 文化の EAFP と例外の使い方 |
| `samples/13_bytecode_and_pycache/` | CPython・バイトコード・`__pycache__` の関係（解説 README 付き） |
| `samples/14_venv_and_dependencies/` | venv・pip・3rd party 依存の隔離（npm との対比、解説 README 付き） |
| `samples/15_python_versions_and_managers/` | `python` / `python3` の使い分け、複数バージョン共存（mise / pyenv / uv、解説 README 付き） |
| `samples/16_tuples.py` | tuple の役割と現場で頻出するパターン（複数戻り値、unpack、dict キー、NamedTuple） |
| `samples/17_http_request_stdlib.py` | 標準ライブラリ `urllib.request` だけで HTTP リクエストを送る |
| `samples/18_http_clients_3rd_party/` | 3rd party HTTP クライアント比較（`requests` / `httpx` / `aiohttp`）と OpenAPI Generator が `requests` を採用しない理由の解説。専用 `pyproject.toml` + `uv` で動かす。`run_all.py` からは除外 |

## 読み進め方

まずは各ファイルをそのまま実行し、出力を見てからコードを読んでください。特に `05_mutability_and_default_args.py`、`07_iterators_generators.py`、`12_eafp_exceptions.py` は、他言語の感覚のままだとバグにしやすいポイントです。
