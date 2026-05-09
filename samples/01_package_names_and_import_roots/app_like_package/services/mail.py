"""メール関連の処理を置いたモジュール。

Java / PHP と違い、ここには `package ...` や `namespace ...` のような所属宣言を書かない。
置き場所が `app_like_package/services/mail.py` なので、import 名は
`app_like_package.services.mail` になる。
"""


def build_subject(user_name: str) -> str:
    return f"ようこそ、{user_name} さん"
