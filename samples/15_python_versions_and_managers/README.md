# 15_python_versions_and_managers

「`python` と `python3` どっちを使えばいい？」「複数バージョンが共存していて厄介」という、Python を始めるとほぼ全員が一度はぶつかる問題を整理するサンプルです。

[14_venv_and_dependencies/](../14_venv_and_dependencies/) が **「依存ライブラリの隔離」** の話だったのに対し、こちらは **「Python 本体（インタプリタ）のバージョン管理」** の話を扱います。

## 実行

```bash
python samples/15_python_versions_and_managers/main.py
```

出力例:

```
# this interpreter
sys.executable : /Users/you/.local/share/mise/installs/python/3.12.13/bin/python
sys.version    : 3.12.13 (main, ...)
sys.prefix     : /Users/you/.local/share/mise/installs/python/3.12.13
sys.base_prefix: /Users/you/.local/share/mise/installs/python/3.12.13
in venv?       : False

# `python` / `python3` resolution on this PATH
  python  : /Users/you/.local/share/mise/shims/python  →  /Users/you/.local/share/mise/bin/mise
  python3 : /Users/you/.local/share/mise/shims/python3 →  /Users/you/.local/share/mise/bin/mise

# version manager hints (presence only)
  mise  : /opt/homebrew/bin/mise
  pyenv : (not installed)
  uv    : /opt/homebrew/bin/uv
  asdf  : (not installed)
  env vars:
    MISE_SHELL = zsh
```

ポイントは:

- `sys.executable` で「いま動いている Python の絶対パス」が分かる
- `python` と `python3` がそれぞれどこに解決されているか・最終的な実体は何か
- どのバージョン管理ツールが入っているかの当たり

## 解説

### 結論

- **2026 年現在、`python` ≒ Python 3 と思って良い**。Python 2 は 2020-01-01 に EOL を迎え、主要 OS からも削除済み
- **`python` で Python 3 が動くようにセットアップするのが正しい運用**。`python3` を使うのは過渡期の名残で、積極的な必然性は薄れている
- 現代の課題は「Python 2 vs 3」ではなく、**「Python 3.x の minor バージョン共存」**

### `python` と `python3` の歴史的経緯

| 時期 | 状況 | `python` が指したもの |
| --- | --- | --- |
| 〜2010s 中盤 | Python 2 が主流 | Python 2 |
| 2010s 後半（移行期） | Python 2/3 共存 | OS によって違う・混乱期 |
| 2020-01 | Python 2 EOL | 多くの OS が `python` を Python 3 に切替 |
| 2022 (macOS 12.3) | `/usr/bin/python` (Py2) を削除 | macOS では `python` 自体が無くなった |
| 2024〜2026 | 主要環境はほぼ Python 3 | **`python` = Python 3 が前提** |

### PEP 394 の方針転換

PEP 394（"The python Command on Unix-Like Systems"）は、過渡期は `python` を Python 2 にしておくよう推奨していたが、**Python 2 の EOL を受けて改訂**され、現在は次の方針:

- `python` は Python 3 を指してよい / 指すべき
- 新しいディストロでは `python` を Python 3 にエイリアスすべき

### `python` / `python3` / `python3.12` の正体は同じ実行ファイル

「`python --version`、`python3 --version`、`python3.12 --version` がすべて同じ Python 3.12 を返す。3 つも入れた覚えはないけど大丈夫？」と思うかもしれないが、**これは普通かつ意図された設計**。Python のインストーラ（python.org / mise / pyenv / Homebrew / OS パッケージ いずれも）が、**1 つの実行ファイルに対して 3 つの名前**を付けてくれているだけ。

実際のディレクトリを見ると symlink で繋がっている:

```bash
$ ls -la "$(dirname "$(which python)")" | grep python
-rwxrwxr-x  ...  python3.12          ← これが本物の実行ファイル
lrwxr-xr-x  ...  python3 -> python3.12
lrwxr-xr-x  ...  python  -> python3.12
```

つまり **物理的にはインタプリタは 1 つだけ**で、残りは別名（symlink）。ディスクも RAM も食わない。

#### なぜ 3 つの名前があるのか

PEP 394 が定める **「3 段階の specificity（具体度）」** を提供するためで、それぞれ役割がある。

| 名前 | 意味 | 想定する用途 |
| --- | --- | --- |
| `python3.12` | **最も具体**: バージョン固定 | 「Python 3.12 でしか動かないスクリプト」「複数 minor 共存環境で明示」 |
| `python3` | **中間**: メジャーだけ固定 | 「Python 3 系ならどれでも動く」（Python 2 と区別する） |
| `python` | **最も汎用**: 区別しない | 「Python ならなんでも動く」、現代では実質 Python 3 |

#### 削除してはいけない

「自分は `python` しか使わないから `python3` / `python3.12` を消したい」と思いがちだが、**消すと色々壊れる**:

| 削除すると壊れるもの | 例 |
| --- | --- |
| 既存スクリプトの shebang | `#!/usr/bin/env python3` で書かれたシステムツール多数 |
| `venv` の生成・利用 | `.venv/bin/` にも `python` / `python3` / `python3.12` の 3 つが同様に作られる |
| `pip` / `pipx` などのコマンド | 内部で `python3` を呼ぶことがある |
| OS / ディストロのシステムツール | apt / dnf / Homebrew 等が依存 |
| CI / Docker | 多くが `python3` を期待 |

つまり **「自分が打つのは `python` だけ」でも、3 つあること自体が他のツールとの互換性を支えている**ので、消すのは損しかない。

#### 実用上の覚え方

- **物理的には 1 つ、別名が 3 つ** — `ls -la $(which python)` で symlink を見れば一目瞭然
- **自分が打つコマンドは `python` で統一して OK**（[このページ冒頭の結論](#結論)）
- **`python3` / `python3.12` は他のツールが裏で使うもの** — 消さずに放置するのが正解
- **「自分でインストールした覚えがない」のは正しい** — Python のインストーラが 1 セットで提供している

`python3.12` を明示的に呼びたくなる場面は実用上ほぼなく、強いて挙げれば「複数 minor が同居していて特定バージョンを呼びたい」「`python3.12 -m venv .venv` のように venv 作成時にバージョンを指定したい」程度。mise / `.tool-versions` で自動切替してしまえばその必要も消える。

### なぜ「`python3` を使う」は対症療法なのか

「`python: command not found` だから `python3` を使う」は短期的には動くが、本質的解決ではない:

| 視点 | 問題 |
| --- | --- |
| **venv の中では `python` が正規名** | `.venv/bin/python` は存在し、`python3` はその symlink。venv ベースの開発をする限り結局 `python` を打つことになる |
| **公式ドキュメント / チュートリアルが `python` を使う** | `python3` を使い続けるとドキュメントとの乖離が生じる |
| **環境のセットアップ問題を先送りしている** | 「無いから別の名前で呼ぶ」ではなく「無いなら入れる」が筋 |
| **チーム内で揃わない** | 各自の習慣がバラバラだと、ドキュメントやスクリプトも揺れる |

### 正しいセットアップ（OS 別）

| 環境 | 推奨アクション | 結果 |
| --- | --- | --- |
| **Ubuntu / Debian** | `sudo apt install python-is-python3` | `/usr/bin/python` が `python3` の symlink になる |
| **Fedora / RHEL** | `sudo alternatives --set python /usr/bin/python3` | `python` が選択した version を指す |
| **macOS（Homebrew）** | デフォルトで `python` が Python 3 を指す | 何もしなくて良い |
| **Windows（python.org installer）** | インストール時に "Add to PATH" を有効化 | `python` で 3 系が動く |
| **mise / pyenv / uv で管理** | これらが提供する shim に `python` がある | プロジェクトで自動切替される |

### 複数バージョン共存問題（3 層モデル）

「Python 2 と 3」ではなく **「Python 3.10 / 3.11 / 3.12 / 3.13 をどう使い分けるか」** が現代の課題。3 層に分けて整理すると見通しが良い。

#### 層 (a): Python 本体のバージョン切り替え

OS の system Python はいじらず、ユーザー領域に複数バージョンを入れて切り替える。

| ツール | 特徴 |
| --- | --- |
| **`uv python install 3.12.13`** | uv が Python 本体の管理機能も持っている。**今から始めるならこれが最も簡単** |
| **`mise`** | 多言語対応（Node, Python, Go まとめて）。`.tool-versions` でプロジェクト固定。最近の人気 |
| **`pyenv`** | Python 専用の老舗。`.python-version` ファイルで自動切替 |
| **`asdf`** | 多言語対応の老舗 |

これらは **プロジェクトに入った瞬間に `python` が自動で目的のバージョンに切り替わる** ように動くため、`python` / `python3` の呼び分けで悩まなくなる。

#### 層 (b): プロジェクトごとの依存とランタイムの隔離

[14_venv_and_dependencies/](../14_venv_and_dependencies/) で扱った話。venv（または uv / Poetry）を作れば、その中の `python` は確実にそのバージョン。

```bash
.venv/bin/python --version   # → 必ず venv 作成時の Python
```

`.venv/bin/python` をフルパスで呼べば、シェルの `python` / `python3` 設定に左右されない。エディタや CI もこのパスを指せば確定的になる。

#### 層 (c): スクリプト / CI / Docker での明示

「他の人にも同じバージョンで動かしてほしい」場面では、書き手側で固定するのが一番安全。

- **Shebang**: チーム内なら `#!/usr/bin/env python` で良い。不特定多数に配るなら `#!/usr/bin/env python3` の方が安全
- **Dockerfile**: `FROM python:3.12.13-slim` のように micro バージョンまで固定
- **CI (GitHub Actions)**: `actions/setup-python@v5` で `python-version: "3.12.13"` を指定
- **README**: 「動作確認バージョン」を明記

### 立場別の正しい解

| あなたの立場 | `python` / `python3` の選択 |
| --- | --- |
| 自分のローカル環境を整える | **`python` = Python 3 になるようセットアップする**。`python3` を使う必要は無い |
| チーム内で共有するスクリプト | `python` で良い（チームの環境整備が前提） |
| 不特定多数に配る OSS スクリプト | shebang は `python3` のほうが安全（受け取り手の環境が古い可能性に備える） |
| Docker / CI | `python` で良い（公式 image / setup-python は両方を Python 3 にする） |

### 補足: 「世の中のツールが `python3` を使ってるから自分も `python3` で書いてよい？」

「Ansible や Homebrew、yt-dlp、各種 OSS の shebang が `#!/usr/bin/env python3` になっている。だったら自分が作るツールも `python3` を前提にして良いのでは？」と思いがち。**結論: 半分正しい。ただし「現代のベストプラクティスだから」ではなく「過去の事情の引きずり」なので、何を作るかで使い分けるのが筋が良い**。

#### 既存ツールが `python3` を使っている本当の理由

「`python3` が正しいから」ではなく、**ほぼ歴史的経緯**:

- 多くの著名ツールは **2010 年代の Python 2/3 移行期** に作られた
- 当時は `python` が Python 2 を指す環境がまだ大量にあったため、Python 3 を確実に呼ぶには `python3` と書くしかなかった
- 一度 `python3` で書かれたツールは、互換性を壊さないために今も `python3` のまま

つまり「`python3` が**正しいから**使われている」のではなく、「**当時の事情で `python3` で書かれてしまった**」ものが多い。残骸的な側面がある。

実際、新しめのツール（uv、Poetry、Ruff の README、最近の OSS の install ドキュメント）は **`python` で書かれていることが多い**。PEP 394 の改訂後はこちらが正論。

#### 配布対象で判断する

「世の中が `python3` だから自分も `python3`」という単純な真似は過剰防衛になりやすい。**配布対象を決めてから shebang を選ぶ**のが正しい順序。

| 配布対象 | shebang | 理由 |
| --- | --- | --- |
| 自分専用 / チーム内 | `#!/usr/bin/env python` | 環境セットアップが揃っている前提 |
| 社内ツール（環境管理あり） | `#!/usr/bin/env python` | mise / Docker などで Python が用意されているなら問題ない |
| **OSS として不特定多数に配布** | `#!/usr/bin/env python3` | 受け取り手の環境が古い／壊れていることに備える |
| 古い Linux サーバー上で動かす | `#!/usr/bin/env python3` | `python` コマンドが無い可能性がある |
| Docker 内 / CI 内でしか動かない | `#!/usr/bin/env python` | 公式 image / setup-python が両方を提供 |

#### shebang の慣習と「自分が打つコマンド」を混同しない

ここが一番大事なポイント。**配布物の shebang と、ターミナルで自分が打つコマンドは別レイヤー**。

```bash
# tools の中身（配布物）
#!/usr/bin/env python3        ← 配布物の互換性のための慣習

# あなたが普段ターミナルで打つこと
python script.py              ← これでまったく問題ない
python -m venv .venv          ← venv 内では python が canonical
```

「OSS で `python3` の shebang を見たから、ターミナル操作も全部 `python3` で打つ」は過剰反応。**普段の操作は `python` で統一して OK**。

#### おすすめスタンス

```diagram
╭──────────────────────────────────────────────╮
│ 配布対象を決めてから shebang を選ぶ          │
├──────────────────────────────────────────────┤
│ 内部利用（自分・チーム・社内）               │
│   → shebang も `python` で OK                │
│                                              │
│ 外部配布（OSS / 不特定多数）                 │
│   → shebang は `python3` で安全側に倒す      │
│                                              │
│ どちらでも、ターミナル操作は `python` 統一   │
╰──────────────────────────────────────────────╯
```

整理すると:

- **「世の中のツールが `python3` を使ってるから自分もそれで良い」は配布物の shebang に限れば妥当**
- **ただし「だから普段のコマンド入力も `python3` にすべき」とまでは言えない** — そこは `python` で良い
- **「`python3` を使うのが現代のベストプラクティス」ではなく「過去の事情の引きずり」だと正しく認識した上で、配布対象を見て選ぶ**のが筋

### 触ってはいけないもの: system Python

特に Linux で **`/usr/bin/python` を直接いじる / `sudo pip install` する** のは厳禁。

- apt / dnf などの OS パッケージ管理が依存している
- 上書きすると OS のスクリプトが壊れることがある
- やりたいことは大抵、ユーザー領域のバージョン管理ツール + venv で実現できる

### よくある事故と対処

| 症状 | 原因 | 対処 |
| --- | --- | --- |
| `python: command not found`（Linux） | OS が `python` を提供していない | `python-is-python3` を入れる、または mise / uv を導入 |
| `python` のバージョンが想定と違う | system / Homebrew / pyenv / mise が混在し、PATH の順番でズレる | `which -a python` で全候補を確認、PATH 順を整理 |
| 同僚と挙動が違う | 各自の `python` のバージョンが違う | `.tool-versions` / `.python-version` / `pyproject.toml` でプロジェクトに宣言 |
| エディタで補完が効かない | エディタが system Python を見ている | エディタのインタプリタを `.venv/bin/python` に固定 |
| スクリプトが手元では動くがサーバーで動かない | 開発機とサーバーで Python バージョンが違う | Docker でバージョンを固定、または CI でテスト |

## まとめ

```diagram
╭───────────────────────────╮
│ 現代 Python の運用方針     │
├───────────────────────────┤
│ ① `python` = Python 3     │ ← セットアップで揃える（python3 で逃げない）
│ ② バージョン管理ツール     │ ← uv / mise / pyenv で複数 minor を共存
│ ③ venv で依存隔離          │ ← samples/14 で扱った話
│ ④ プロジェクトで宣言       │ ← .tool-versions, pyproject.toml, Dockerfile
╰───────────────────────────╯
```

「`python` と `python3` で混乱する」のは、本質的には **環境セットアップの問題**であって、コマンド名の選び方の問題ではない、というのがこのサンプルの主張です。

## 参考情報

- [PEP 394 – The "python" Command on Unix-Like Systems](https://peps.python.org/pep-0394/)
- [Python 2.7 EOL announcement (PSF)](https://www.python.org/doc/sunset-python-2/)
- [`python-is-python3` (Ubuntu)](https://packages.ubuntu.com/jammy/python-is-python3)
- [uv: Installing and managing Python](https://docs.astral.sh/uv/concepts/python-versions/)
- [mise documentation](https://mise.jdx.dev/)
- [pyenv](https://github.com/pyenv/pyenv)
- [Docker Official Image: python](https://hub.docker.com/_/python)
