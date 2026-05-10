# 55_tooling_ruff_black_mypy_pyright

Python 業務開発でよく見る開発ツールの位置づけを整理するサンプルです。

このリポジトリは標準ライブラリだけで動くサンプル集なので、Ruff / Black / mypy / pyright 自体は導入しません。ここでは「何をする道具なのか」だけを扱います。

## ざっくり分類

| 種類 | 役割 | 代表例 |
| --- | --- | --- |
| formatter | コードの見た目を自動整形する | Black, Ruff formatter |
| linter | 未使用 import、危険な書き方、スタイル逸脱を検出する | Ruff, Flake8, Pylint |
| type checker | 型ヒントを静的解析する | mypy, pyright |

## PEP 8 との関係

PEP 8 は Python の基本スタイルガイドです。ただし実務では、人間が細かい整形ルールをすべて覚えて手作業で守るより、formatter / linter に任せることが多いです。

## Java 経験者向けの対応イメージ

- formatter: google-java-format など
- linter: Checkstyle / PMD / SpotBugs 的な役割の一部
- type checker: Java のコンパイル時型チェックに少し近いが、Python では型ヒントを元にした静的解析であり、実行時に強制されるわけではない

## 動かし方

```bash
python samples/55_tooling_ruff_black_mypy_pyright/main.py
```
