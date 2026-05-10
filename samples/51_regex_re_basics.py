"""標準ライブラリ `re` の基本: search / match / fullmatch / group。

Python の正規表現は `re` モジュールで扱う。Java の Pattern / Matcher に近いが、
Python では `r"..."` の raw string でパターンを書くのが定番。
"""

import re


def main() -> None:
    text = "user=alice email=alice@example.com status=active"

    print("--- raw string で正規表現を書く ---")
    # `\d` や `\w` のような backslash を Python 文字列側で解釈させないため、r"..." を使う。
    number_pattern = re.compile(r"\d+")
    print(number_pattern.findall("order-100 and order-250"))

    print("\n--- search は文字列の途中も探す ---")
    email_pattern = re.compile(r"(?P<user>[a-z]+)@(?P<domain>[\w.]+)")
    match = email_pattern.search(text)
    if match is not None:
        print(f"email: {match.group(0)}")
        print(f"user : {match.group('user')}")
        print(f"domain: {match.group('domain')}")

    print("\n--- match は先頭から一致するかを見る ---")
    print(re.match(r"user=", text) is not None)
    print(re.match(r"email=", text) is not None)

    print("\n--- fullmatch は文字列全体が一致するかを見る ---")
    print(re.fullmatch(r"[a-z]+", "alice") is not None)
    print(re.fullmatch(r"[a-z]+", "alice123") is not None)

    print("\n--- 使いすぎ注意 ---")
    print("  CSV / JSON / HTML など専用 parser がある形式は、正規表現だけで頑張りすぎない")


if __name__ == "__main__":
    main()
