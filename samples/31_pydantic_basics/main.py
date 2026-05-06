"""Pydantic v2 の基本: 実行時 validation と型変換。

Pydantic は標準ライブラリではないが、FastAPI などの Web API 開発で頻出する。
このサンプルは専用 uv プロジェクトとして動かす前提で、scripts/run_all.py からは除外している。

動かし方:

    cd samples/31_pydantic_basics
    uv sync
    uv run main.py
"""

try:
    import pydantic
    from pydantic import BaseModel, ConfigDict, Field, ValidationError
except ImportError:
    print("Pydantic v2 が入っていません。")
    print("cd samples/31_pydantic_basics && uv sync && uv run main.py で実行してください。")
    raise SystemExit(0)

if not pydantic.__version__.startswith("2."):
    print(f"Pydantic v2 用のサンプルです（現在: {pydantic.__version__}）。")
    print("cd samples/31_pydantic_basics && uv sync && uv run main.py で実行してください。")
    raise SystemExit(0)


class Item(BaseModel):
    # alias は外部 JSON の key と Python 側の属性名を分けたいときに使う。
    product_id: str = Field(alias="productId", min_length=1)
    name: str
    price: int = Field(ge=0)


class Order(BaseModel):
    # extra="forbid" にすると、想定外の key をエラーにできる。
    # populate_by_name=True にすると、alias だけでなく Python 側の属性名でも入力できる。
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    order_id: str = Field(alias="orderId")
    items: list[Item]
    coupon_code: str | None = Field(default=None, alias="couponCode")


class StrictPrice(BaseModel):
    # strict=True にすると、"1200" -> 1200 のような暗黙変換を禁止する。
    model_config = ConfigDict(strict=True)

    price: int


def main() -> None:
    raw_order = {
        "orderId": "ord-001",
        "items": [
            {"productId": "book", "name": "Python Book", "price": "1200"},
            {"productId": "pen", "name": "Pen", "price": 200},
        ],
    }

    print("--- dict / JSON 相当の入力を model に変換 ---")
    order = Order.model_validate(raw_order)
    print(order)
    print(f"price の型: {type(order.items[0].price).__name__}")

    print("\n--- model から dict に戻す ---")
    print(order.model_dump(by_alias=True))

    print("\n--- validation error ---")
    try:
        Order.model_validate({"orderId": "ord-002", "items": [], "unexpected": "NG"})
    except ValidationError as error:
        print(error.errors()[0])

    print("\n--- strict mode ---")
    try:
        StrictPrice.model_validate({"price": "1200"})
    except ValidationError as error:
        print(error.errors()[0])


if __name__ == "__main__":
    main()
