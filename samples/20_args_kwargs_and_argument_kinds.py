"""`*args` / `**kwargs` と引数種別（positional-only / keyword-only）。

Python の関数定義は引数の渡し方を細かく制御できる:

- 通常の引数  : 位置でもキーワードでも渡せる
- `/`         : これより前は positional-only（キーワードでは渡せない）
- `*`         : これより後は keyword-only（位置では渡せない）
- `*args`     : 余った位置引数を tuple で受ける
- `**kwargs`  : 余ったキーワード引数を dict で受ける

他言語と比べると:

- Java     : メソッドオーバーロードは型で分岐するが、Python には無い
- Go       : 可変長引数 `args ...T` はあるが、キーワード引数自体が無い
- TypeScript: rest parameter `...args` はあるが、keyword-only の概念は弱い
- Python は「呼び出し側のスタイル」を関数側で強制できるのが特徴
"""


# ============================================================
# *args と **kwargs
# ============================================================
# `*args` は「余った位置引数を tuple で受ける」、
# `**kwargs` は「余ったキーワード引数を dict で受ける」、という慣習名。
# 名前は `*things`, `**options` のように何でもよいが、慣例として args / kwargs を使う。
def show_all(*args: object, **kwargs: object) -> None:
    print(f"  args   = {args}")    # tuple
    print(f"  kwargs = {kwargs}")  # dict


# ============================================================
# *args / **kwargs を「中継」する典型例（decorator / wrapper でよく出る）
# ============================================================
def add(a: int, b: int) -> int:
    return a + b


def call_twice(func, *args, **kwargs):
    # 受け取った引数をそのまま透過的に渡せる。decorator の中身がだいたいこれ。
    func(*args, **kwargs)
    func(*args, **kwargs)


# ============================================================
# positional-only ( / ) と keyword-only ( * )
# ============================================================
# `/` より前 : 位置でしか渡せない
# `/` と `*` の間: 位置でもキーワードでも渡せる
# `*` より後 : キーワードでしか渡せない
#
# 例: greet(greeting, name, /, *, loud=False)
#   - greeting, name は位置のみ
#   - loud は必ずキーワード指定（greet("Hi", "Bob", True) は TypeError）
#
# なぜ使い分けるか:
#   - positional-only にすると、引数名を将来変えても呼び出し側を壊さない
#   - keyword-only にすると、bool フラグなどの「意味が分かりにくい引数」を
#     必ず `loud=True` のように明示させられる（可読性 / API の安全性が上がる）
def greet(greeting: str, name: str, /, *, loud: bool = False) -> str:
    message = f"{greeting}, {name}!"
    return message.upper() if loud else message


# ============================================================
# 呼び出し側での * / ** unpack
# ============================================================
# 関数定義の `*args` / `**kwargs` と対称に、
# 呼び出し側でも list/tuple を `*` で展開、dict を `**` で展開できる。
def make_url(scheme: str, host: str, path: str) -> str:
    return f"{scheme}://{host}{path}"


def main() -> None:
    print("--- *args / **kwargs ---")
    show_all(1, 2, 3, name="Alice", role="admin")

    print("\n--- 引数を中継する wrapper ---")
    call_twice(add, 1, 2)  # add(1, 2) を 2 回呼ぶ
    # 直接出力させたいので print を渡す
    call_twice(print, "hello", "world", sep="-")

    print("\n--- positional-only / keyword-only ---")
    print(greet("Hello", "Alice"))                 # OK
    print(greet("Hi", "Bob", loud=True))            # OK
    # greet("Hi", "Bob", True)        → TypeError（loud は keyword-only）
    # greet(greeting="Hi", name="Bob") → TypeError（greeting/name は positional-only）

    print("\n--- 呼び出し側の * / ** unpack ---")
    parts = ["https", "example.com", "/index.html"]
    options = {"scheme": "https", "host": "example.com", "path": "/about"}
    print(make_url(*parts))     # list を位置引数に展開
    print(make_url(**options))  # dict をキーワード引数に展開


if __name__ == "__main__":
    main()
