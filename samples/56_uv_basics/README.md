# 56_uv_basics

`uv` の基本的な使い方を整理するサンプルです。

`uv` は Python の標準ライブラリではありませんが、2024〜2026 年の Python 開発では急速に普及しているツールです。Python 本体のインストール、仮想環境、依存解決、lock ファイル、コマンド実行を 1 つの CLI で扱えます。

このリポジトリは標準ライブラリだけで動くサンプル集なので、`uv` 自体は依存として追加しません。`main.py` はコマンド一覧を表示するだけです。

## 実行

```bash
python samples/56_uv_basics/main.py
```

## uv は何を置き換えるのか

Python は歴史的に、用途ごとに別々のツールを組み合わせることが多いです。

| やりたいこと | 従来の代表例 | uv での代表例 |
| --- | --- | --- |
| Python 本体を入れる | python.org installer / pyenv / mise | `uv python install 3.12` |
| 仮想環境を作る | `python -m venv .venv` | `uv venv` または `uv sync` |
| 依存を追加する | `pip install requests` | `uv add requests` |
| 依存を固定する | `requirements.txt` / pip-tools | `uv.lock` |
| lock から環境を再現する | `pip install -r requirements.txt` | `uv sync` |
| プロジェクト環境で実行する | `.venv/bin/python main.py` | `uv run python main.py` |
| CLI ツールを単発実行する | pipx / npx 的な使い方 | `uv tool run ruff check .` |

Node.js 経験者には、ざっくり次のように捉えると近いです。

| Node.js / npm | uv |
| --- | --- |
| `package.json` | `pyproject.toml` |
| `package-lock.json` | `uv.lock` |
| `npm install` | `uv sync` |
| `npm install <pkg>` | `uv add <pkg>` |
| `npm run ...` / `npx ...` | `uv run ...` / `uv tool run ...` |
| `nvm install` | `uv python install` |

## 最小ワークフロー

新しい Python プロジェクトを `uv` で始める最小例です。

```bash
# 1. プロジェクトを作る
uv init hello-uv
cd hello-uv

# 2. Python バージョンを用意する
uv python install 3.12

# 3. 依存を追加する
uv add requests

# 4. プロジェクトの環境で実行する
uv run python main.py
```

`uv add requests` を実行すると、主に次が更新されます。

- `pyproject.toml`: 直接依存として `requests` が記録される
- `uv.lock`: 依存の依存まで含めて、解決済みバージョンが記録される
- `.venv/`: プロジェクト用の仮想環境が作成・更新される

`.venv/` は生成物なので git 管理しません。一方、`pyproject.toml` と `uv.lock` はチームで同じ環境を再現するために git 管理するのが普通です。

## 既存プロジェクトを動かす

すでに `pyproject.toml` と `uv.lock` があるプロジェクトでは、基本は次だけです。

```bash
uv sync
uv run python main.py
```

`uv sync` は lock ファイルに従って `.venv/` を作り直します。つまり「このリポジトリで決められた依存バージョンを、自分の PC に再現する」操作です。

## `uv run` の便利さ

従来の venv では、次のように仮想環境を有効化してから実行することが多いです。

```bash
python -m venv .venv
source .venv/bin/activate
python main.py
```

`uv run` を使うと、activate を省略できます。

```bash
uv run python main.py
```

`uv run` は「このプロジェクトの `.venv` を使ってコマンドを実行する」と読めます。CI や README の手順では、シェルの状態に依存しにくいので便利です。

## 依存の追加と削除

```bash
uv add requests
uv remove requests
```

開発時だけ使うツールは dev dependency に入れます。

```bash
uv add --dev ruff
uv run ruff check .
```

ただし、このリポジトリ自体には Ruff などを導入しません。ツールの位置づけは [55_tooling_ruff_black_mypy_pyright](../55_tooling_ruff_black_mypy_pyright/) で扱っています。

## 一時的に CLI ツールを使う

プロジェクトの依存に追加せず、単発で CLI を実行したい場合は `uv tool run` を使えます。

```bash
uv tool run ruff check .
```

これは Node.js の `npx` や Python の `pipx run` に近い使い方です。短く `uvx ruff check .` と書ける環境もあります。

## 注意点

- `uv` は標準ライブラリではないため、使うプロジェクトではインストール手順を README に書く
- `.venv/` は git 管理しない
- `uv.lock` は再現性のために git 管理する
- ライブラリとして公開するパッケージでは、利用者側の解決余地を残すため lock の扱いをプロジェクト方針で決める
- `pip` / `venv` の知識が不要になるわけではない。uv の裏側でも Python の仮想環境と package metadata の考え方は使われている

## 参考情報

- [uv documentation](https://docs.astral.sh/uv/)
- [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/)
- [Python Packaging User Guide: pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
