"""`pickle` の便利さと危険性。

pickle は Python オブジェクトを Python 専用の形式で直列化できる標準ライブラリ。
業務では「ある時点の Python オブジェクトを bytes にして、ファイル・DB・Redis などに保存し、
後で復元して再利用する」用途で見かけることがある。
便利だが、信頼できないデータを `pickle.loads()` / `pickle.load()` してはいけない。
"""

import json
import pickle
from dataclasses import dataclass


@dataclass
class UserSession:
    user_id: int
    roles: list[str]


def main() -> None:
    session = UserSession(user_id=123, roles=["admin", "editor"])

    print("--- pickle は Python オブジェクトをそのまま保存しやすい ---")
    payload = pickle.dumps(session)
    restored = pickle.loads(payload)
    print(f"restored: {restored}")
    print(f"type(restored): {type(restored).__name__}")
    print(f"payload type: {type(payload).__name__}")

    print("\n--- 業務で見かける利用イメージ ---")
    print("  1. pickle.dumps(obj) で Python オブジェクトを bytes にする")
    print("  2. その bytes をファイル・DB の BLOB カラム・Redis などに保存する")
    print("  3. 後で取り出した bytes を pickle.loads(...) で Python オブジェクトに戻す")
    print("  例: 計算済みオブジェクトのキャッシュ、ジョブの中間状態、Python 内部だけで使う一時保存")

    print("\n--- JSON は言語をまたぎやすいが、表現できる型は限定的 ---")
    json_payload = json.dumps({"user_id": session.user_id, "roles": session.roles})
    print(json_payload)
    print(json.loads(json_payload))

    print("\n--- pickle の注意点 ---")
    print("  - Python 専用で、長期保存や他言語連携には向きにくい")
    print("  - クラス定義の場所や名前が変わると、古い pickle を読めなくなることがある")
    print("  - Redis / DB / ファイルに保存した pickle でも、出どころを信頼できないなら load しない")
    print("  - 読み込み時に任意コード実行につながり得るため、信頼できない pickle は絶対に load しない")
    print("  - 外部入力には JSON など、安全に扱いやすい形式を優先する")


if __name__ == "__main__":
    main()
