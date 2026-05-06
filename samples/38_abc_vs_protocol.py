"""`abc.ABC` と `Protocol` の使い分け: nominal vs structural typing。

Python では「明示的に継承したか」を見る設計と、
「必要なメソッドを持っているか」を見る設計を使い分ける。
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


class PaymentGateway(ABC):
    # ABC は nominal typing。「PaymentGateway を継承したもの」を要求する。
    @abstractmethod
    def charge(self, amount: int) -> str:
        raise NotImplementedError


class StripeGateway(PaymentGateway):
    def charge(self, amount: int) -> str:
        return f"stripe charged {amount}"


@runtime_checkable
class CanCharge(Protocol):
    # Protocol は structural typing。「charge を持つもの」を要求する。
    def charge(self, amount: int) -> str: ...


class FakeGateway:
    # PaymentGateway は継承していないが、charge を持つので CanCharge として扱える。
    def charge(self, amount: int) -> str:
        return f"fake charged {amount}"


def checkout(gateway: CanCharge, amount: int) -> None:
    print(gateway.charge(amount))


def main() -> None:
    stripe = StripeGateway()
    fake = FakeGateway()

    print("--- ABC: 明示的な継承 ---")
    print(isinstance(stripe, PaymentGateway))
    print(isinstance(fake, PaymentGateway))

    print("\n--- Protocol: 構造で見る ---")
    print(isinstance(stripe, CanCharge))
    print(isinstance(fake, CanCharge))

    print("\n--- 利用側は CanCharge だけを要求する ---")
    checkout(stripe, 1000)
    checkout(fake, 1000)


if __name__ == "__main__":
    main()
