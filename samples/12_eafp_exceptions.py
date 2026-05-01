"""EAFP: Easier to Ask Forgiveness than Permission。

Python では「事前にできるか確認する」より、「まず試して失敗したら例外で扱う」
スタイルがよく使われます。もちろん外部境界の入力検証は別問題です。
"""


def parse_port(config: dict[str, str]) -> int:
    try:
        port = int(config["port"])
    except KeyError:
        print("port is missing, use default")
        return 8000
    except ValueError:
        print("port is not an integer, use default")
        return 8000
    else:
        print("port was parsed successfully")
        return port
    finally:
        print("parse_port finished")


def main() -> None:
    print(parse_port({"port": "8080"}))
    print(parse_port({}))
    print(parse_port({"port": "not-a-number"}))


if __name__ == "__main__":
    main()
