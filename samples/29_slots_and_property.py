"""`__slots__` と `@property`: クラス設計の Python 流イディオム。

Python のインスタンスは普段 `__dict__` という辞書に属性を保持していて、
**実行時に好きな属性をいくらでも追加できる** のが特徴（他の言語と一番違う点）。

- `__slots__` を宣言すると、`__dict__` を作らずに属性を固定する
  → メモリ削減 + 「タイポした属性を勝手に追加してしまう」事故を防ぐ
- `@property` は「メソッドを属性のように見せる」仕組み
  → 後から「単純な属性」を「validation 付きの属性」に差し替えてもインターフェースが変わらない

dataclass(slots=True) (3.10+) を使うと、この 2 つを一緒に活用できる。
"""

from dataclasses import dataclass


# ============================================================
# 普通のクラス: 属性をいくらでも生やせる
# ============================================================
class LooseUser:
    def __init__(self, name: str) -> None:
        self.name = name


# ============================================================
# __slots__ を宣言したクラス
# ============================================================
# ここで宣言した属性以外を代入しようとすると AttributeError。
# - メモリ削減: __dict__ を作らない（多数のインスタンスを持つときに効く）
# - バグ防止 : self.naem = "..." のようなタイポを実行時に検出できる
class StrictUser:
    __slots__ = ("name", "age")

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


# ============================================================
# @property: メソッドを属性のように見せる
# ============================================================
# 最初は単純な属性として書き始め、後で「validation を追加したい」「読み取り専用にしたい」
# となったときに、呼び出し側のコードを変えずに property に差し替えられる。
# Java の getter/setter の代替だが、呼び出し側は p.celsius のように属性アクセスのまま。
class Temperature:
    def __init__(self, celsius: float) -> None:
        # 内部状態は慣習として _celsius のようにアンダースコア接頭辞を付ける。
        # （Python に private はない。「触らないでね」という強い慣習のみ。）
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        # ゲッター。t.celsius でこのメソッドが呼ばれる（() を付けない）。
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        # セッター。t.celsius = -300 のような代入時に呼ばれる。
        # ここで validation を入れられる。
        if value < -273.15:
            raise ValueError(f"絶対零度より低い温度は不可: {value}")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        # 計算で求まる「派生プロパティ」。setter を定義しなければ読み取り専用。
        return self._celsius * 9 / 5 + 32


# ============================================================
# dataclass(slots=True): __slots__ を自動で付けてくれる
# ============================================================
# 3.10+ で `slots=True` オプションが追加された。
# 普通の dataclass + 属性固定 + メモリ効率を一度に得られる。
@dataclass(slots=True)
class Point:
    x: float
    y: float


def main() -> None:
    print("--- 普通のクラス: 属性を勝手に追加できる ---")
    loose = LooseUser("alice")
    loose.role = "admin"  # 何のエラーも出ない
    loose.naem = "BOB"     # タイポしても気付けない
    print(f"  loose.name = {loose.name}")
    print(f"  loose.role = {loose.role}")
    print(f"  loose.naem = {loose.naem}  ← タイポが事故になる")

    print("\n--- __slots__ で属性を固定 ---")
    strict = StrictUser("alice", 30)
    print(f"  strict.name = {strict.name}, strict.age = {strict.age}")
    try:
        strict.role = "admin"  # __slots__ に無いので AttributeError
    except AttributeError as e:
        print(f"  AttributeError: {e}")

    print("\n--- @property: 属性アクセスのままで validation ---")
    t = Temperature(25)
    print(f"  t.celsius    = {t.celsius}      # () を付けない")
    print(f"  t.fahrenheit = {t.fahrenheit}   # 派生プロパティ")

    t.celsius = 100
    print(f"  100 を設定後: celsius={t.celsius}, fahrenheit={t.fahrenheit}")

    try:
        t.celsius = -300  # setter の validation で弾かれる
    except ValueError as e:
        print(f"  ValueError: {e}")

    try:
        t.fahrenheit = 100  # setter を定義していないので AttributeError
    except AttributeError as e:
        print(f"  AttributeError: {e}")

    print("\n--- @dataclass(slots=True) ---")
    p = Point(1.0, 2.0)
    print(f"  p = {p}")
    try:
        p.z = 3.0
    except AttributeError as e:
        print(f"  AttributeError: {e}")


if __name__ == "__main__":
    main()
