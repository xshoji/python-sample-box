"""`unittest` 入門: 標準ライブラリだけでテストを書く。

Python の現場では pytest も非常に人気だが、標準ライブラリだけで完結する
`unittest` を知っておくと、依存を増やせない環境や既存コードで役に立つ。
"""

import sys
import unittest


def normalize_name(name: str) -> str:
    if not name.strip():
        raise ValueError("name は空にできません")
    return name.strip().lower()


class NormalizeNameTest(unittest.TestCase):
    def test_strip_and_lower(self) -> None:
        self.assertEqual(normalize_name(" Alice "), "alice")

    def test_empty_name_raises(self) -> None:
        with self.assertRaises(ValueError):
            normalize_name("   ")

    def test_subtest(self) -> None:
        # subTest は似た入力をまとめて検証したいときに便利。
        cases = ["Bob", " BOB ", "bob"]
        for value in cases:
            with self.subTest(value=value):
                self.assertEqual(normalize_name(value), "bob")


def main() -> None:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(NormalizeNameTest)
    # TextTestRunner の既定出力先は stderr。
    # サンプル実行時に順番が分かりやすいよう、ここでは stdout に出す。
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
