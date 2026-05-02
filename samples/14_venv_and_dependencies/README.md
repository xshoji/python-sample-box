# 14_venv_and_dependencies

3rd party ライブラリを「サーバー（system Python）を汚さずに」プロジェクト単位でインストールする方法をまとめたサンプルです。

Node.js の `node_modules` / npm に慣れている人向けに、Python での相当物を整理します。

## 実行

このサンプル自体は **3rd party 依存ゼロ** で動きます。`sys` / `site` の情報を表示するだけです。

```bash
python samples/14_venv_and_dependencies/main.py
```

出力例（venv 未使用 = system Python の場合）:

```
# interpreter location
sys.executable   : /opt/homebrew/opt/python@3.12/bin/python3.12
sys.prefix       : /opt/homebrew/opt/python@3.12/Frameworks/Python.framework/Versions/3.12
sys.base_prefix  : /opt/homebrew/opt/python@3.12/Frameworks/Python.framework/Versions/3.12

# venv?
running on the *system* / non-venv Python
→ pip install するとこの Python 全体に影響します
```

このあと後述の手順で venv を作って `python samples/14_venv_and_dependencies/main.py` を再実行すると、`sys.prefix` が `.venv/...` を指し、`running inside a virtual environment` と出るはずです。**「venv に切り替わるとは何が切り替わることか」** を出力で見比べてみてください。

## 解説

### Python は何もしないと「サーバー全体」に入る

`pip install requests` は、**いま `python` として呼ばれている Python の `site-packages/` に**ライブラリを書き込みます。

- ローカル PC で `python` が system Python を指していれば、PC の system Python が汚れる
- サーバーで `sudo pip install` をすると、**OS パッケージ管理（apt / dnf / brew）と同じ Python に混入**して OS を壊しうる（特に Linux）
- バージョン違いの依存を持つプロジェクトを 2 つ並べると、片方が壊れる

つまり Python では **「プロジェクトごとに専用の Python 環境を作る」のが前提** です。

### 標準解: `venv`（Python 3.3+ 標準同梱）

プロジェクト直下に **専用の Python 実行ファイル + 専用の `site-packages/`** を作る仕組みです。npm の `node_modules` に最も近い感覚で使えます。

```bash
# 1. プロジェクト直下に venv を作る
python -m venv .venv

# 2. 有効化（macOS / Linux）
source .venv/bin/activate
#    Windows (PowerShell) なら: .venv\Scripts\Activate.ps1
#    Windows (cmd) なら:        .venv\Scripts\activate.bat

# 3. このシェルでは python / pip が .venv 配下のものに切り替わる
which python    # → .../your-project/.venv/bin/python
pip install requests   # → .venv 配下にだけ入る

# 4. 抜ける
deactivate
```

仕組みのポイント:

- `.venv/bin/python` は **system Python へのリンクと専用の sys.prefix** を持つ Python 実行ファイル
- `activate` は単に **`PATH` の先頭に `.venv/bin` を差し込むシェル関数** にすぎない
- だから `activate` を使わなくても `./.venv/bin/python script.py` のようにフルパスで呼べば同じこと
- **`.venv/` は git 管理しない**（このリポジトリの [.gitignore](file:///Users/user/Develop/ghq/github.com/xshoji/python-sample-box/.gitignore) に `.venv` が入っています）

### 依存関係の固定: `requirements.txt`

npm の `package.json`（の dependencies）に近い、**素朴な依存リスト**です。

```bash
# 現在の venv に入っているものを書き出す
pip freeze > requirements.txt

# 別の環境で再現する
pip install -r requirements.txt
```

`requirements.txt` の中身は単なるテキスト:

```
requests==2.32.3
urllib3==2.2.3
```

ただし **lock ファイル相当の機能はない**（依存の依存まで厳密に固定する標準仕組みがない）ため、再現性が必要なプロジェクトでは後述のツールに移行するのが普通です。

### npm との対応表

| npm | Python（venv + pip） | 備考 |
| --- | --- | --- |
| `node_modules/` | `.venv/lib/pythonX.Y/site-packages/` | 隔離の場所 |
| `package.json` (deps) | `requirements.txt` または `pyproject.toml` | 入れたいものリスト |
| `package-lock.json` | （素の pip にはない） | uv / Poetry なら lock ファイルあり |
| `npm install` | `pip install -r requirements.txt` | |
| `npx <cmd>` | `python -m <module>` / `pipx run <cmd>` | 単発実行 |
| `nvm` | `pyenv` / `uv python install` | Python 本体のバージョン切替 |

### より新しい選択肢

| ツール | 立ち位置 | 特徴 |
| --- | --- | --- |
| **`uv`** | 2024〜2025 で急速に普及 | Rust 製で爆速。`uv venv` / `uv add` / `uv lock` / `uv run` が揃い、npm に近い感覚で使える。**今から始めるならこれが第一候補** |
| Poetry | 一時期のデファクト | `pyproject.toml` + `poetry.lock`。安定だが速度面で uv に押されつつある |
| PDM | 軽量寄り | PEP 準拠重視 |
| Pipenv | 古参 | 推奨度は下がった |

`uv` での例（venv を意識しなくて済む）:

```bash
uv init                    # pyproject.toml を作る
uv add requests            # 依存を追加（lock も自動更新）
uv run python main.py      # プロジェクトの環境で実行
uv sync                    # lock に従って依存を再現
```

### 開発ツール（lint / formatter / type checker）の置き場

開発時にしか使わないツール（`ruff` / `black` / `mypy` 等）も、**venv に入れる**のが基本です。`pip install` 系では `requirements-dev.txt` を分けたり、Poetry / uv では「dev dependencies」グループを使います。

グローバルに常駐させたいツール（`black` をどこからでも呼びたい等）には、**`pipx`** が定番です。`pipx install black` で「専用 venv にインストール + コマンドだけ PATH に通す」を自動でやってくれます。

### よくある事故

| 症状 | 原因 | 対策 |
| --- | --- | --- |
| `sudo pip install` で OS が不安定に | system Python を上書きした | system Python に直接 `pip install` しない。venv か `pipx` を使う |
| 別プロジェクトに切り替えたら import エラー | venv を有効化し忘れている | `which python` で `.venv/bin/python` を指しているか確認 |
| `requirements.txt` 通りに入れたのに動かない | 間接依存のバージョンが違う | uv / Poetry の lock を使う |
| エディタで補完が効かない | エディタが system Python を見ている | エディタのインタプリタ設定を `.venv/bin/python` に向ける |

## 参考情報

- [Python docs: venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Python Packaging User Guide: Installing packages using pip and virtual environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
- [pip docs: Requirements File Format](https://pip.pypa.io/en/stable/reference/requirements-file-format/)
- [pipx](https://pipx.pypa.io/)
- [uv documentation](https://docs.astral.sh/uv/)
- [Poetry documentation](https://python-poetry.org/docs/)
