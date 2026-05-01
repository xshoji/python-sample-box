"""`dataclass` による値オブジェクト的なクラス。

Python では単にデータを運ぶクラスを書く場面が多くあります。
`dataclass` は `__init__`、`__repr__`、比較などの定型実装を生成します。
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class Money:
    amount: int
    currency: str = "JPY"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("amount must be non-negative")


@dataclass
class Invoice:
    customer: str
    lines: list[Money] = field(default_factory=list)

    def total(self) -> Money:
        return Money(sum(line.amount for line in self.lines))


def main() -> None:
    invoice = Invoice("alice")
    invoice.lines.append(Money(1200))
    invoice.lines.append(Money(800))

    print(invoice)
    print(invoice.total())
    print(Money(100) < Money(200))


if __name__ == "__main__":
    main()
