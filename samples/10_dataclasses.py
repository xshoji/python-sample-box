"""`dataclass` による値オブジェクト的なクラス。

Python では単にデータを運ぶクラスを書く場面が多くあります。
`dataclass` は `__init__`、`__repr__`、比較などの定型実装を生成します。
"""

from dataclasses import dataclass, field


# ============================================================
# @dataclass のオプション
# ============================================================
# @dataclass を付けると、クラス変数の宣言から __init__ / __repr__ / __eq__ などを
# 自動生成してくれる（Java の record、Kotlin の data class、TypeScript の interface +
# class boilerplate に近い）。
#
# よく使うオプション:
#   frozen=True : 生成されたインスタンスを immutable にする。
#                 - インスタンス生成後に obj.amount = 999 のような代入をすると
#                   FrozenInstanceError を投げる。
#                 - 副次効果として __hash__ も自動生成され、set / dict のキーに使えるようになる。
#                 - 「値オブジェクト」（Money, Coordinate, Color など）を定義するときの定番。
#
#   order=True  : <, <=, >, >= の比較演算子を自動生成する。
#                 - 比較は「フィールドを宣言順に tuple として並べたものを比較する」挙動。
#                 - 例: Money(100, "JPY") < Money(200, "JPY")  → True
#                       Money(100, "JPY") < Money(100, "USD")  → True (currency で比較)
#                 - 大小比較が意味を持つ値オブジェクトのときだけ付ける。
#
# 他のオプションには eq / repr / unsafe_hash / slots / kw_only などがある。
@dataclass(frozen=True, order=True)
class Money:
    amount: int
    currency: str = "JPY"  # デフォルト値があるフィールドは、無いフィールドより後ろに置く必要がある

    # ============================================================
    # __post_init__: dataclass 専用の「__init__ の直後フック」
    # ============================================================
    # @dataclass が生成する __init__ は、引数を self.<field> に代入するだけのシンプルな実装。
    # その「自動生成された __init__ の最後」に呼ばれるのが __post_init__。
    # 主にバリデーションや派生フィールドの計算に使う。
    #
    # フローを擬似コードで書くと:
    #   def __init__(self, amount, currency="JPY"):
    #       self.amount = amount
    #       self.currency = currency
    #       self.__post_init__()      # ← @dataclass がここを自動で挿入する
    #
    # 普通のクラスで __init__ の中に直接書くようなチェックを、dataclass では
    # __post_init__ に書く、という住み分け。
    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("amount must be non-negative")


@dataclass
class Invoice:
    customer: str

    # ============================================================
    # field(default_factory=list) とは
    # ============================================================
    # 「デフォルト値として list を持たせたい」場合、`lines: list[Money] = []` と書きたくなるが、
    # それは samples/05_mutability_and_default_args.py で見た「mutable デフォルトの罠」と
    # 同じ問題（全インスタンスが同じ list を共有してしまう）を起こすため、
    # @dataclass は宣言時に明示的に禁止していて ValueError を投げる。
    #
    # 代わりに使うのが `field(default_factory=<callable>)`。
    # - default_factory には「呼び出すと初期値を返す関数」を渡す（list, dict, set, lambda 等）。
    # - インスタンス生成のたびに factory が呼ばれ、新しい list / dict が割り当てられる。
    #
    # 例:
    #   tags:    set[str]       = field(default_factory=set)
    #   meta:    dict[str, str] = field(default_factory=dict)
    #   created: datetime       = field(default_factory=datetime.utcnow)
    #
    # field() には他にも repr / compare / metadata / kw_only などの細かい制御がある。
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
