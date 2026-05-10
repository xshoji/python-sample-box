"""標準ライブラリ `sqlite3`: DB 操作と SQL injection 回避の入口。

Python には SQLite クライアントが標準ライブラリとして入っている。
本格的な業務アプリでは SQLAlchemy などを使うことも多いが、DB API の基本を確認するには便利。
"""

import sqlite3
from contextlib import closing


def main() -> None:
    print("--- in-memory DB を作る ---")
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.row_factory = sqlite3.Row

        # `with connection:` は transaction の commit / rollback を管理する。
        with connection:
            connection.execute("create table users (id integer primary key, name text, role text)")
            connection.executemany(
                "insert into users (name, role) values (?, ?)",
                [("alice", "admin"), ("bob", "viewer"), ("carol", "viewer")],
            )

        print("\n--- placeholder `?` を使って値を渡す ---")
        role = "viewer"
        rows = connection.execute(
            "select id, name, role from users where role = ? order by id",
            (role,),
        ).fetchall()
        for row in rows:
            print(dict(row))

        print("\n--- SQL 文字列に値を直接埋め込まない ---")
        unsafe_input = "viewer' or '1' = '1"
        safe_rows = connection.execute(
            "select id, name from users where role = ?",
            (unsafe_input,),
        ).fetchall()
        print(f"placeholder を使うと、不正な入力は単なる値として扱われる: {len(safe_rows)} 件")

    print("\nconnection は closing(...) により close 済み")


if __name__ == "__main__":
    main()
