"""3rd party HTTP クライアントの比較サンプルを順に実行するエントリポイント。

このディレクトリ配下には次のサンプルが入っている。

- requests_example.py : `requests`（同期、デファクト）
- httpx_example.py    : `httpx`（同期 + 非同期、2026 年の新規第一候補）
- aiohttp_example.py  : `aiohttp`（非同期専用、サーバも同梱）

正規の動かし方:

    cd samples/18_http_clients_3rd_party
    uv sync          # .venv をこの dir に作って依存を入れる
    uv run main.py   # 全部を順に実行

`requests`/`httpx`/`aiohttp` のどれかが入っていない状態で実行された場合は、
そのサンプルだけスキップして続行する（直接 `python main.py` で叩かれた場合の保険）。

scripts/run_all.py からはこのサンプル全体を除外している。
"""

from __future__ import annotations

import importlib


# 実行する順番に並べた example モジュール名。
EXAMPLES = ("requests_example", "httpx_example", "aiohttp_example")


def main() -> None:
    for name in EXAMPLES:
        print(f"\n========= {name} =========")
        try:
            module = importlib.import_module(name)
        except ModuleNotFoundError as exc:
            # 該当の 3rd party が入っていないだけ。スキップして次へ。
            print(f"  skip ({name}): missing dependency '{exc.name}'")
            print("  hint: uv sync (in samples/18_http_clients_3rd_party)")
            continue
        module.main()


if __name__ == "__main__":
    main()
