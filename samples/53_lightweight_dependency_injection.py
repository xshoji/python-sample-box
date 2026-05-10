"""Python で DI を軽くやる: 関数引数、コンストラクタ引数、`Protocol`。

Java / Spring のような DI コンテナを想像しがちだが、Python ではまず
「必要な依存を引数で渡す」だけで十分な場面が多い。型としては `Protocol` を使うと、
明示的な継承なしに「必要なメソッドを持つもの」を表せる。
"""

from typing import Protocol


class Notifier(Protocol):
    def send(self, message: str) -> None: ...


class OrderRepository(Protocol):
    def save(self, order_id: str, amount: int) -> None: ...


class ConsoleNotifier:
    def send(self, message: str) -> None:
        print(f"通知: {message}")


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[str, int] = {}

    def save(self, order_id: str, amount: int) -> None:
        self.orders[order_id] = amount


class CheckoutService:
    def __init__(self, repository: OrderRepository, notifier: Notifier) -> None:
        self.repository = repository
        self.notifier = notifier

    def checkout(self, order_id: str, amount: int) -> None:
        self.repository.save(order_id, amount)
        self.notifier.send(f"order_id={order_id}, amount={amount} を保存しました")


class FakeNotifier:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)


def main() -> None:
    print("--- 実装を外から渡す ---")
    repository = InMemoryOrderRepository()
    service = CheckoutService(repository=repository, notifier=ConsoleNotifier())
    service.checkout("order-001", 3000)
    print(repository.orders)

    print("\n--- テストでは fake を渡す ---")
    fake_notifier = FakeNotifier()
    test_repository = InMemoryOrderRepository()
    test_service = CheckoutService(repository=test_repository, notifier=fake_notifier)
    test_service.checkout("order-002", 1200)
    print(fake_notifier.messages)

    print("\nPython では DI コンテナより先に、引数で依存を渡す設計を考えることが多い")


if __name__ == "__main__":
    main()
