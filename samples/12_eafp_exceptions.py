"""EAFP: Easier to Ask Forgiveness than Permission。

Python では「事前にできるか確認する」より、「まず試して失敗したら例外で扱う」
スタイルがよく使われます。もちろん外部境界の入力検証は別問題です。
"""


# ============================================================
# KeyError / ValueError は Python の組み込み例外
# ============================================================
# Python は import なしで使える「組み込み例外（built-in exceptions）」を多数持つ。
# Java で言う `java.lang.*` の例外クラス群、Go の `errors` パッケージで定義された
# 標準エラーに近い位置付け。すべて BaseException を頂点とする継承ツリーに属している。
#
#   BaseException
#    └─ Exception                  ← 普通のアプリ例外はだいたいこの下
#        ├─ LookupError
#        │   ├─ KeyError           ← dict に存在しない key を参照したとき
#        │   └─ IndexError         ← list / tuple の範囲外を参照したとき
#        ├─ ValueError             ← 型は正しいが値が不正（例: int("abc")）
#        ├─ TypeError              ← 型自体が不正（例: "a" + 1）
#        ├─ AttributeError         ← 存在しない属性を参照（obj.no_such_attr）
#        ├─ FileNotFoundError      ← open() で存在しないファイルを開く
#        ├─ ZeroDivisionError      ← 0 で割った
#        ├─ StopIteration          ← iterator が尽きた（generator の内部で使われる）
#        └─ ...（他にも多数）
#
# 全一覧: https://docs.python.org/ja/3/library/exceptions.html
#
# 自作例外を作るときは Exception を継承するのが慣例:
#   class MyAppError(Exception): ...
#
# この parse_port では、組み込み例外を 2 種類「使い分けて」捕まえている:
#   - config["port"] が無いとき   → dict[] のアクセスが KeyError を投げる
#   - "abc" のような値だったとき → int("abc") が ValueError を投げる
# このように「何が起きたか」で例外型が分かれているので、except 節で
# 適切に分岐できる、というのが Python 標準ライブラリの設計思想。
def parse_port(config: dict[str, str]) -> int:
    try:
        port = int(config["port"])
    except KeyError:
        # config に "port" キーが無いと、config["port"] の時点で KeyError。
        print("port is missing, use default")
        return 8000
    except ValueError:
        # config["port"] は取れたが、int() に渡せない文字列だと ValueError。
        print("port is not an integer, use default")
        return 8000
    else:
        # try ブロックが例外なく終わったときだけ実行される。
        print("port was parsed successfully")
        return port
    finally:
        # 例外の有無に関係なく、必ず最後に実行される（return より後に走る点に注意）。
        print("parse_port finished")


def main() -> None:
    print(parse_port({"port": "8080"}))
    print(parse_port({}))
    print(parse_port({"port": "not-a-number"}))


if __name__ == "__main__":
    main()
