"""設定の扱い: 環境変数、型変換、`tomllib`、設定オブジェクト。

Java の application.properties / application.yml 的な設定は、Python では環境変数、
TOML / JSON / YAML、dataclass、Pydantic などを組み合わせて扱うことが多い。
ここでは標準ライブラリだけで、環境変数と TOML を設定オブジェクトにまとめる。
"""

import os
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    debug: bool
    port: int
    database_url: str
    retry_count: int


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"bool として解釈できません: {value!r}")


def load_from_env(env: Mapping[str, str]) -> AppConfig:
    # Mapping は「dict そのもの」ではなく、「key で value を読み取れる dict 風のもの」を表す抽象型。
    # Java の `Map<String, String>` を読み取り用途で受け取る感覚に近い。
    #
    # ここを `dict[str, str]` に限定すると、普通の dict だけを想定した API に見える。
    # `Mapping[str, str]` にしておくと、テスト用の dict も、実際の os.environ も受け取れる。
    # os.environ は通常の dict ではなく環境変数と連動する特殊な object だが、
    # `get()` / `[]` / `in` などで dict のように読めるので Mapping として扱える。
    # 環境変数は常に文字列。int / bool などは自分で変換する。
    return AppConfig(
        debug=parse_bool(env.get("APP_DEBUG", "false")),
        port=int(env.get("APP_PORT", "8000")),
        database_url=env.get("DATABASE_URL", "sqlite:///local.db"),
        retry_count=int(env.get("RETRY_COUNT", "3")),
    )


def load_from_toml(text: str) -> AppConfig:
    data = tomllib.loads(text)
    app = data["app"]
    return AppConfig(
        debug=app["debug"],
        port=app["port"],
        database_url=app["database_url"],
        retry_count=app["retry_count"],
    )


def main() -> None:
    print("--- 環境変数から設定を作る ---")
    fake_env = {
        "APP_DEBUG": "true",
        "APP_PORT": "8080",
        "DATABASE_URL": "postgresql://db.example/app",
        "RETRY_COUNT": "5",
    }
    print(load_from_env(fake_env))
    # isinstance(..., Mapping) で、os.environ が「dict 風に読める object」かを確認している。
    print(f"実際の os.environ も Mapping[str, str] として扱える: {isinstance(os.environ, Mapping)}")

    print("\n--- TOML から設定を作る ---")
    toml_text = """
[app]
debug = false
port = 9000
database_url = "sqlite:///app.db"
retry_count = 2
"""
    print(load_from_toml(toml_text))

    print("\n--- 補足 ---")
    print("  .env ファイルは標準ライブラリだけでは自動読み込みされない")
    print("  実務では python-dotenv や Pydantic Settings などを使うことも多い")


if __name__ == "__main__":
    main()
