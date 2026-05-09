# 48_entry_points_and_main_module

Python の代表的な実行入口を確認するサンプルです。

## 扱う入口

- `python path/to/file.py`
- `python -m package.module`
- `python -m package` で使われる `package/__main__.py`
- `pyproject.toml` の `[project.scripts]` による console script

## ポイント

`python file.py` は、指定したファイルを直接スクリプトとして実行します。

一方、`python -m package.module` は、import できるモジュール名を指定して実行します。パッケージ内部の相対 import や import 探索を考えると、アプリケーションコードでは `-m` 実行の方が自然な場面があります。

`python -m package` のように package 名だけを指定した場合は、`package/__main__.py` が実行されます。

console script は、インストール時にコマンド名と Python 関数を結びつける仕組みです。例えば次の設定は、`demo-command` というコマンドから `demo_pkg.cli.main` を呼ぶ、という意味になります。

```toml
[project.scripts]
demo-command = "demo_pkg.cli:main"
```

## 動かし方

```bash
python samples/48_entry_points_and_main_module/main.py
```
