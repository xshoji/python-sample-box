# サンプル追加候補リスト

このリポジトリに今後追加していけそうなサンプルテーマの **ブレスト用ドラフト** です。
AI エージェントや人間が「次に何を書くか」を判断するときの参照ドキュメントとして使います。

- 対象: Python 3.12 系（このリポジトリの方針に合わせる）
- 既存サンプル: `samples/01_*` 〜 `samples/48_*` を踏まえた上での追加候補
- 採用方針: **他言語経験者がつまずく Python 固有の概念**、または **業務 / OSS で頻出するパターン** を優先
- 制約: AGENTS.md のルール（3rd party 禁止、日本語コメント、`NN_snake_case`、ディレクトリ形式は `main.py` をエントリポイントにする 等）に従う

---

## A. 言語コアでまだ拾えていないもの（優先度高め）

| # | テーマ | 概要 |
|---|---|---|
| A1 | `*args` / `**kwargs` と引数種別 | positional-only `/` と keyword-only `*` の文法。API 設計で必須 |
| A2 | `match` 文（structural pattern matching, 3.10+） | dict / dataclass の分解マッチ。Java `switch` や Rust `match` との対比 |
| A3 | `enum.Enum` / `StrEnum` / `IntEnum`（3.11 で `StrEnum`） | 業務頻出。Java enum との違い（メソッド・比較） |
| A4 | `pathlib.Path` | `os.path` ではなく `pathlib` が現代的。`/` 演算子でのパス連結 |
| A5 | `logging` 入門 | `print` ではなく logger を使う理由、`getLogger(__name__)`、`basicConfig` の落とし穴 |
| A6 | `datetime` / `zoneinfo`（3.9+）と naive vs aware | 業務で必ず踏むタイムゾーンの罠 |
| A7 | f-string 詳細 | `{value=}` debug、書式指定、`%` formatting / `.format()` との比較 |
| A8 | `collections` 系 | `defaultdict`, `Counter`, `deque`, `namedtuple`, `ChainMap` |
| A9 | `itertools` / `functools` 厳選 | `chain`, `groupby`, `accumulate`, `pairwise`(3.10+) / `lru_cache`, `cache`, `partial`, `reduce` |
| A10 | `typing` 実用編 | `Protocol`（structural typing）、`TypedDict`、`Literal`、`NewType`、`Final`、`overload`、`TYPE_CHECKING` |
| A11 | `Optional[T]` と `T | None`、`Union` と `|`（3.10+） | 型の書き分け |
| A12 | ジェネリクス（PEP 695, 3.12+） | `def first[T](xs: list[T]) -> T:` |
| A13 | `asyncio` 入門 | `async def` / `await` / `asyncio.run` / `gather`、同期コードと混ぜる際の落とし穴 |
| A14 | `concurrent.futures` と GIL | `ThreadPoolExecutor` vs `ProcessPoolExecutor`、GIL を 1 ファイルで |
| A15 | `subprocess.run` の正しい使い方 | `shell=True` の危険、`check=True`、`capture_output=True` |
| A16 | `__slots__` | メモリ最適化と attribute 動的追加禁止。dataclass との併用 |
| A17 | descriptor / `@property` / `@classmethod` / `@staticmethod` | `property` の getter / setter validation の作法 |

---

## B. 標準ライブラリ・OSS でよく出る実装パターン

| # | テーマ | 概要 |
|---|---|---|
| B1 | `abc.ABC` / `abstractmethod` と Protocol の使い分け | nominal vs structural typing |
| B2 | `contextlib` 応用 | `@contextmanager`, `ExitStack`, `suppress`, `closing` |
| B3 | `json` / `csv` 標準ライブラリ | `json.dumps(..., default=...)` の話含む |
| B4 | `argparse` で CLI を作る | 業務頻出、標準ライブラリで完結 |
| B5 | `unittest` 入門 | 3rd party 禁止ルールに従い `pytest` ではなく `unittest` で書く |
| B6 | `__all__` と公開 API の制御 | `from pkg import *` の挙動 |
| B7 | `sys.path` / `PYTHONPATH` / 相対 import vs 絶対 import | import の事故とその回避 |
| B8 | `weakref` | キャッシュやオブザーバパターンで使う |
| B9 | `copy.copy` / `copy.deepcopy` | shallow / deep の違い |
| B10 | `pickle` の使いどころと危険性 | 信頼できないデータの load 禁止 |

---

## C. ソフトウェアアーキテクチャ・パターン的な話

| # | テーマ | 概要 |
|---|---|---|
| C1 | Pythonic ビフォーアフター集 | `for i in range(len(xs))` → `enumerate`、ネスト for → 内包表記など。1 ファイルに 5〜10 例まとめ |
| C2 | EAFP の発展形：自作例外クラスの設計 | 既存例外の継承、エラー階層 |
| C3 | DI を「軽く」やる | DI コンテナを入れず、関数引数 / `Protocol` / `partial` で十分 |
| C4 | 設定の扱い | `os.environ`, `dataclass` で設定オブジェクト化, `.env` を標準ライブラリで読む |
| C5 | plugin / registry パターン | decorator で関数を辞書に登録（Flask の route が代表例） |

---

## D. プロジェクト構成・運用（14, 15, 18, 19 の延長）

| # | テーマ | 概要 |
|---|---|---|
| D1 | `pyproject.toml` の最小構成（PEP 621） | `setup.py` 時代との比較 |
| D2 | `src/` レイアウト vs flat レイアウト | import 事故を防ぐ src/ レイアウト |
| D3 | `ruff` / `black` / `mypy` / `pyright` | 説明のみ。AGENTS.md の lint 追加禁止ルールがあるため README で触れるに留める |
| D4 | エントリポイント | `python -m pkg`、`__main__.py`、`pyproject.toml` の `[project.scripts]` |
| D5 | `uv` / `pipx` / `poetry` / `rye` | 15 の補強として 1 ファイル比較表 |

---

## 推奨採用候補（厳選 8〜10 本）

「他言語経験者が一番つまずく順」で並べた、最初に書くと価値が高いもの。
**20〜48 は実装済み**（2026-05 時点）。A7 の f-string 詳細は、細かい仕様説明になりやすいため現時点では採用を見送った。

| 番号 | テーマ | ステータス | 採用理由 |
|---|---|---|---|
| 20 | `*args` / `**kwargs` と positional-only / keyword-only | 実装済み | 既存 05（mutable default）と並ぶ「引数の落とし穴」枠 |
| 21 | `match` 文 | 実装済み | 3.10+ 固有、強力なのに知らない人が多い |
| 22 | `enum`（`Enum`, `StrEnum`） | 実装済み | 業務頻出、Java enum との比較も書きやすい |
| 23 | `pathlib` | 実装済み | `os.path` 文化からの移行を明示 |
| 24 | `logging` の基本作法 | 実装済み | `print` デバッグ卒業。`getLogger(__name__)` 慣習 |
| 25 | `datetime` / `zoneinfo` と naive vs aware | 実装済み | 業務で確実に踏む地雷 |
| 26 | `typing` 実用編（`Protocol` / `TypedDict` / `Literal`） | 実装済み | 既存 11 の続編。OSS でよく見る型注釈 |
| 27 | `asyncio` 最小サンプル | 実装済み | 概念だけでも触れておく価値が高い |
| 28 | `argparse` で CLI を作る | 実装済み | 標準ライブラリだけで完結、業務頻出 |
| 29 | `__slots__` と `@property` | 実装済み | クラス設計の Python 流イディオム |
| 30 | `self` / `@staticmethod` / `@classmethod` | 実装済み | クラスの第1引数、状態に依存しない処理、代替コンストラクタの使い分け |
| 31 | Pydantic v2 基本 | 実装済み | FastAPI などの業務 API 開発で頻出。型注釈と実行時 validation の違いを示せる |
| 32 | `json` / `csv` 標準ライブラリ | 実装済み | 外部データ入出力で頻出。Pydantic との接続もしやすい |
| 33 | `collections` 系 | 実装済み | `Counter` / `defaultdict` / `deque` など、実務で使うと意図が伝わりやすい |
| 34 | `itertools` / `functools` 厳選 | 実装済み | Python らしい iterator ベースのデータ処理に慣れる |
| 35 | `subprocess.run` の正しい使い方 | 実装済み | CLI / batch / automation で頻出。`shell=True` の危険も説明できる |
| 36 | `concurrent.futures` と GIL | 実装済み | I/O 並行と CPU 並列の使い分けを理解できる |
| 37 | `unittest` 入門 | 実装済み | 3rd party を増やせない環境でも使える標準テスト機能 |
| 38 | `abc.ABC` と `Protocol` の使い分け | 実装済み | nominal typing と structural typing の違いを整理できる |
| 39 | `contextlib` 応用 | 実装済み | `with` 文を実務パターンに広げられる |
| 40 | `pyproject.toml` / `src` レイアウト | 実装済み | 現代的な Python プロジェクト構成の入口になる |
| 41 | public / private / protected を命名規約で表す Python 文化 | 実装済み | PEP 8 由来の `_name` / `__name` / `__all__` の慣習を整理できる |
| 42 | `Optional[T]` と `T | None`、`Union` と `|` | 実装済み | None を含む型、Union、省略可能な引数の違いは実務で頻出 |
| 43 | ジェネリクス（PEP 695, 3.12+） | 実装済み | 3.12 前提の新構文として、旧 TypeVar との比較を示せる |
| 44 | `copy.copy` / `copy.deepcopy` | 実装済み | mutable object の参照共有と shallow / deep の違いはバグになりやすい |
| 45 | `pickle` の使いどころと危険性 | 実装済み | 標準ライブラリだが、信頼できないデータの load 禁止は重要 |
| 46 | Pythonic ビフォーアフター集 | 実装済み | 他言語の癖から Python らしい書き方へ移る入口になる |
| 47 | EAFP の発展形：自作例外クラスの設計 | 実装済み | 既存例外・自作例外・例外 chaining の使い分けを示せる |
| 48 | エントリポイント | 実装済み | `python -m pkg`、`__main__.py`、console script の関係を整理できる |

---

## 未確定の判断ポイント

このリストから実装に進む前に、以下は人間に確認したい：

1. **優先順位**: A / B / C / D のどこを厚くするか
2. **`pytest` の扱い**: 3rd party 禁止ルールに従い `unittest` で 1 本書くか、README で触れるだけにするか
3. **`asyncio` の粒度**: 1 ファイル or `samples/NN_asyncio/` ディレクトリ形式
4. **`pyproject.toml` / `src/` レイアウト**: ディレクトリ形式のサンプル増を許容するか
5. **Pythonic ビフォーアフター集（C1）**: 1 ファイルに 5〜10 例まとめる形で採用するか
