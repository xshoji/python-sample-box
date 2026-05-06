"""`self` / `@staticmethod` / `@classmethod` の使い分け。

Python の通常メソッドでは、第1引数に「呼び出し元インスタンス自身」が渡されます。
その第1引数を `self` と名付けるのが強い慣習です。

一方で、インスタンス状態を使わない処理では `@staticmethod`、
クラス自身を使う生成処理では `@classmethod` を使うことがあります。
"""


class UserProfile:
    # 業務コードでの使い分けの目安:
    # - インスタンスごとの状態を読む / 書くなら、通常メソッドにして `self` を書く。
    # - インスタンス状態もクラス状態も使わない補助関数なら、`@staticmethod` で `self` を書かない。
    # - 「そのクラスから作る」処理やサブクラス対応の生成処理なら、`@classmethod` で `cls` を受け取る。
    def __init__(self, user_id: int, display_name: str) -> None:
        # `self` は「いま操作している UserProfile インスタンス自身」。
        # `UserProfile(1, "alice")` のように生成すると、Python が第1引数として自動的に渡す。
        # 文法上 `self` は予約語ではないが、業務ではほぼ必ず `self` という名前を使う。
        self.user_id = user_id
        self.display_name = display_name

    def rename(self, display_name: str) -> None:
        # `profile.rename("alice")` と呼ぶと、`self` には `profile` が入る。
        # JavaScript / Java / Kotlin / C# の `this` に近い。
        self.display_name = display_name

    def summary(self) -> str:
        # `self` 経由で、そのインスタンスが持つ属性を参照する。
        return f"UserProfile(user_id={self.user_id}, display_name={self.display_name!r})"

    def method_without_self(display_name: str) -> None:
        # これは「self を省略できる」という意味ではなく、あえて間違った例。
        # `profile.method_without_self()` と呼ぶと、暗黙に渡された `profile` が `display_name` に入ってしまう。
        # `profile.method_without_self("alice")` と呼ぶと、暗黙の `profile` + 明示した "alice" の2引数になり TypeError。
        print(f"self を書かない通常メソッド: display_name の実体は {type(display_name).__name__}")

    @staticmethod
    def normalize_display_name(display_name: str) -> str:
        # `@staticmethod` はインスタンスを自動で受け取らないので `self` を書かなくてよい。
        # 業務では「クラスの近くに置きたいが、状態には依存しない処理」に使う。
        return display_name.strip().lower()

    @classmethod
    def guest(cls) -> "UserProfile":
        # `@classmethod` はインスタンスではなくクラス自身を `cls` として受け取る。
        # 業務では「代替コンストラクタ」や、サブクラスでも同じ生成処理を使いたい場合に使う。
        return cls(user_id=0, display_name="guest")


def main() -> None:
    profile = UserProfile.guest()
    print(profile.summary())

    normalized = UserProfile.normalize_display_name(" Alice ")
    profile.rename(normalized)
    print(profile.summary())

    # staticmethod はインスタンスから呼んでも、`self` は自動で渡されない。
    print(profile.normalize_display_name(" Bob "))

    profile.method_without_self()
    try:
        profile.method_without_self("alice")
    except TypeError as error:
        print(f"self を書かない通常メソッドに引数を渡すと: {error}")


if __name__ == "__main__":
    main()
