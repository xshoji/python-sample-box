"""public / private / protected を命名規約で表す Python 文化。

Python には Java / PHP / C# のような厳密なアクセス修飾子はない。
代わりに PEP 8 でも説明されている命名規約を使い、公開 API と内部実装を区別する。

この規約は Python コミュニティ全体でかなり広く共有されているが、
言語処理系がアクセスを禁止するわけではない。プロジェクトごとの約束もあり得る。
"""

__all__ = ["UserProfile"]


class UserProfile:
    def __init__(self, name: str) -> None:
        self.name = self._normalize_name(name)
        self._display_count = 0
        self.__audit_token = "created-by-user-profile"

    def display_name(self) -> str:
        """アンダースコアなしの名前は、利用者に公開する API として扱う。"""
        self._display_count += 1
        return self.name.title()

    def _normalize_name(self, name: str) -> str:
        """先頭 `_` は internal / protected 的な慣習。外部利用は避けてほしい合図。"""
        if not name.strip():
            raise ValueError("name は空にできません")
        return name.strip().lower()

    def __audit_label(self) -> str:
        """先頭 `__` は private ではなく、name mangling の対象。"""
        return f"{self.name}:{self.__audit_token}"

    def debug_audit_label(self) -> str:
        """サンプル出力用に、クラス内部から `__audit_label` を呼ぶ。"""
        return self.__audit_label()


class _InternalFormatter:
    """先頭 `_` のクラス名は、モジュール内部用という慣習。"""

    def format(self, value: str) -> str:
        return f"[{value}]"


class BaseJob:
    def run(self) -> str:
        # BaseJob.__step は name mangling により _BaseJob__step として扱われる。
        return self.__step()

    def __step(self) -> str:
        return "BaseJob の内部 step"


class CustomJob(BaseJob):
    def __step(self) -> str:
        # BaseJob.__step とは別名になるので、BaseJob.run() からは呼ばれない。
        return "CustomJob の内部 step"


def main() -> None:
    user = UserProfile(" Alice ")

    print("# 1. public: アンダースコアなし")
    print(f"  user.display_name(): {user.display_name()!r}")

    print("\n# 2. _single_underscore: 内部用という合図だが、アクセスは禁止されない")
    print(f"  user._display_count: {user._display_count}")
    print(f"  user._normalize_name(' BOB '): {user._normalize_name(' BOB ')!r}")
    print("  呼べるが、外部コードが依存すべき API ではない")

    print("\n# 3. __double_underscore: private ではなく name mangling")
    print(f"  user.debug_audit_label(): {user.debug_audit_label()!r}")
    print(f"  hasattr(user, '__audit_label'): {hasattr(user, '__audit_label')}")
    print(f"  hasattr(user, '_UserProfile__audit_label'): {hasattr(user, '_UserProfile__audit_label')}")
    print("  `__name` はサブクラスとの名前衝突を避ける用途が主目的")

    print("\n# 4. name mangling はサブクラスの同名メソッドと衝突しにくくする")
    job = CustomJob()
    print(f"  CustomJob().run(): {job.run()!r}")
    print("  CustomJob.__step ではなく、BaseJob.__step が呼ばれている")

    print("\n# 5. __all__ は `from module import *` の公開対象を示す")
    print(f"  __all__: {__all__}")
    print("  ただし `_InternalFormatter` も、明示的に import すれば使えてしまう")

    print("\n# まとめ")
    print("  Python の public / private / protected は強制ではなく、広く共有された命名文化")


if __name__ == "__main__":
    main()
