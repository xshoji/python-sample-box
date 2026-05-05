# AGENTS.md

このファイルは、このリポジトリで作業する AI エージェント向けの最小限の指示書です。

## リポジトリ概要

`python-sample-box` は、Python 固有の挙動・文化（EAFP、内包表記、context manager、decorator、`__pycache__`、venv など）を、他言語経験者が短時間で掴めるようにした **学習用サンプル集** です。各サンプルは説明よりも「実行して挙動を確認できる」ことを優先します。

- 対象 Python: **3.12 系**（動作確認は 3.12.13）
- 依存: **標準ライブラリのみ**。3rd party は導入しない（`14_venv_and_dependencies` の説明上の例を除く）
- 自然言語: コメント・README・新規ドキュメントは **日本語** で書く
- 想定読者: Java / Go / Node.js などの経験者

## ディレクトリ構成

```
samples/
  NN_name.py            # 単一ファイル形式のサンプル
  NN_name/              # 解説 README や補助モジュールを伴う形式
    main.py             # エントリポイント（固定名）
    README.md           # テーマ解説
  supporting_module_for_import.py  # 03 で使う import 対象
scripts/
  run_all.py            # samples/ を NN 順に一括実行
docs/
  sample_candidates.md  # 今後追加候補のサンプルテーマ一覧（ブレスト用）
README.md               # サンプル一覧と Python バージョン解説
```

## 追加サンプルの検討

新しいサンプルを追加するときは、まず [`docs/sample_candidates.md`](docs/sample_candidates.md) を参照すること。
追加候補のテーマと採用理由、未確定の判断ポイントが整理されている。
新しい候補を思いついた場合もここに追記する。

## サンプルの規約

新規サンプルや既存サンプルを編集する際は次を守ること。

- **1 ファイル 1 テーマ**。混ぜない
- ファイル/ディレクトリ名は `NN_snake_case`（`NN` はゼロ詰め2桁の連番）
- 解説 README や補助モジュールが必要なテーマは `samples/NN_name/` ディレクトリ形式にし、エントリポイントは **必ず `main.py`**（`scripts/run_all.py` がこの規約に依存している）
- 先頭にモジュール docstring（`"""..."""`）でテーマと意図を日本語で書く
- コードは `python samples/NN_xxx.py` または `python samples/NN_xxx/main.py` でそのまま実行できること（追加の引数・環境変数を要求しない）
- `print()` で挙動が分かる出力を出す。出力例はコメントで併記してよい
- 他言語（Java / Go / JavaScript / TypeScript）との対比をコメントに残すと価値が上がる
- 型ヒントは積極的に使うが、「実行時チェックではない」という Python の前提に沿う（`11_type_hints_are_not_runtime_checks.py` 参照）

## コーディングスタイル

- Python 3.12 の機能まで使ってよい（`match`、PEP 695 ジェネリクス等）
- インデントはスペース 4。タブ禁止
- 文字列は基本ダブルクォート、docstring は `"""..."""`
- `from __future__ import annotations` は **原則使わない**。3.12 前提なので `list[str]` や `int | None` はそのまま書ける。自己参照型などやむを得ない場合のみ使う
- 例外を握りつぶさない。EAFP を示すサンプルでは、捕まえる例外型を具体的に書く

## 検証方法

変更後は以下で動作確認すること。

```bash
python --version                       # 3.12.x であることを確認
python samples/<変更したファイル>      # 個別実行
python scripts/run_all.py              # 全サンプルを順に実行（壊れていれば非0終了）
```

`scripts/run_all.py` は `subprocess.run(..., check=True)` で実行するため、どれか 1 つでも失敗すると全体が落ちる。新規追加・修正後は必ず通すこと。

## やらないこと

- 3rd party ライブラリの追加（`pip install`、`requirements.txt`、`pyproject.toml` の新設など）
- ビルドツール・lint・formatter 設定の追加（明示的な依頼があった場合のみ）
- 既存サンプルの番号の振り直し（差分が大きくなり学習者の参照が壊れる）
- `samples/` 配下の `__pycache__/` のコミット（`.gitignore` で除外済みの想定）
- 英語化。コメントは日本語のままにする
