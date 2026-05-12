"""`abc.ABC` と `Protocol` の使い分け: nominal vs structural typing。

Python では「明示的に継承したか」を見る設計と、
「必要なメソッドを持っているか」を見る設計を使い分ける。
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


class PaymentGateway(ABC):
    # ABC は nominal typing。「PaymentGateway を継承したもの」を要求する。
    # Java / TypeScript の interface に近い「契約」を、実行時にも持たせたい場合に使う。
    # @abstractmethod が残っているクラスはインスタンス化できず、
    # サブクラス側に charge の実装を強制できる。
    # つまり「たまたま同じメソッドを持つ」だけではなく、
    # 「この抽象基底クラスの仲間として設計された型」を区別したいとき向き。
    @abstractmethod
    def charge(self, amount: int) -> str:
        raise NotImplementedError


class StripeGateway(PaymentGateway):
    def charge(self, amount: int) -> str:
        return f"stripe charged {amount}"


@runtime_checkable
class CanCharge(Protocol):
    # Protocol は structural typing。「charge を持つもの」を要求する。
    # `...` は Ellipsis（省略記号）という実際の Python オブジェクト。
    # 型定義や Protocol では「ここでは実装を書かず、シグネチャだけ示す」意図でよく使う。
    # この例では `pass` と同じように本体を空にできるが、
    # 「未実装の型契約だけを書いている」と読み取りやすい。
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
    # StripeGateway は PaymentGateway を継承しているので True。
    print(isinstance(stripe, PaymentGateway))
    # FakeGateway は charge を持つが、継承していないので False。
    # ABC は「形が同じか」ではなく「明示的に仲間だと宣言したか」を見る。
    print(isinstance(fake, PaymentGateway))

    print("\n--- Protocol: 構造で見る ---")
    print(isinstance(stripe, CanCharge))
    print(isinstance(fake, CanCharge))

    print("\n--- 利用側は CanCharge だけを要求する ---")
    checkout(stripe, 1000)
    checkout(fake, 1000)


if __name__ == "__main__":
    main()
