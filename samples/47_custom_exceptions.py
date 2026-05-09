"""自作例外クラスの設計: EAFP の発展形。

Python では既存例外を使える場面も多いが、ドメイン上の失敗を呼び出し側で
まとめて扱いたいときは、自作例外クラスを用意すると意図が明確になる。
"""


class PaymentError(Exception):
    """支払い処理全体の基底例外。呼び出し側はこの型でまとめて捕まえられる。"""


class InsufficientBalanceError(PaymentError):
    """残高不足。"""



class PaymentGatewayError(PaymentError):
    """外部決済サービスとの通信・応答に関する失敗。"""


def charge(balance: int, amount: int) -> int:
    if amount <= 0:
        raise ValueError("amount は正の整数である必要があります")
    if balance < amount:
        raise InsufficientBalanceError(f"残高不足: balance={balance}, amount={amount}")
    return balance - amount


def call_gateway() -> None:
    try:
        int("not a status code")
    except ValueError as error:
        # 低レベルの例外を、ドメインに近い例外へ変換する。
        # `from error` により原因の traceback も保持される。
        raise PaymentGatewayError("決済サービスの応答を解釈できません") from error


def main() -> None:
    print("--- 成功 ---")
    print(charge(balance=1000, amount=300))

    print("\n--- 自作例外を個別に捕まえる ---")
    try:
        charge(balance=100, amount=300)
    except InsufficientBalanceError as error:
        print(f"残高不足として処理: {error}")

    print("\n--- 基底例外でまとめて捕まえる ---")
    try:
        call_gateway()
    except PaymentError as error:
        print(f"支払い系の失敗として処理: {error}")
        print(f"原因の型: {type(error.__cause__).__name__}")

    print("\n--- 既存例外で十分な場合もある ---")
    try:
        charge(balance=1000, amount=0)
    except ValueError as error:
        print(f"引数不正: {error}")


if __name__ == "__main__":
    main()
