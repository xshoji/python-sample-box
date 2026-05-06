# 31_pydantic_basics

Pydantic v2 の最小サンプルです。Pydantic は Python 標準ライブラリではありませんが、FastAPI を中心とした Web API 開発、外部 API レスポンスの検証、設定値の validation でよく使われます。

このディレクトリは独立した uv プロジェクトです。リポジトリ全体の「標準ライブラリ中心」方針に影響しないよう、`scripts/run_all.py` からは除外しています。

## 動かし方

```bash
cd samples/31_pydantic_basics
uv sync
uv run main.py
```

## dataclass / TypedDict / Pydantic の違い

| 選択肢 | 主な役割 | 実行時 validation |
| --- | --- | :-: |
| `TypedDict` | dict の形を静的解析に教える | ✗ |
| `dataclass` | 軽量な値オブジェクトを書く | ✗（自前実装） |
| Pydantic `BaseModel` | 外部入力を検証し、型付き object に変換する | ✓ |

## 業務でよく出る使いどころ

- HTTP request / response body の schema validation
- JSON / dict / message queue payload の検証
- OpenAPI / JSON Schema との連携
- 環境変数や設定ファイルの読み込み（`pydantic-settings`）

逆に、単純な内部データ構造だけなら `dataclass` で十分なことも多いです。
