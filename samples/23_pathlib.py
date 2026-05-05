"""`pathlib`: 現代的なファイルパス操作。

`os.path` の関数群（`os.path.join`、`os.path.dirname` など）を、
`Path` オブジェクトのメソッドとしてまとめ直したのが `pathlib`。

ポイント:

- パス連結は `/` 演算子で書ける（OS の区切り文字を意識しなくていい）
- 「存在するか」「ファイルか」「ディレクトリか」を `.exists()` 等で問う
- 読み書きも `Path.read_text()` / `Path.write_text()` で 1 行
- glob / iterdir で配下を走査できる

他言語と比べると Java の `java.nio.file.Path`、Node.js の `path` モジュールに相当するが、
**読み書き API までセットになっている** のが pathlib の便利さ。
"""

import tempfile
from pathlib import Path


def main() -> None:
    # ============================================================
    # パスの作り方と / 演算子による連結
    # ============================================================
    # 文字列を Path() でラップする。連結は + ではなく / を使う。
    base = Path("/var/log")
    log_path = base / "app" / "today.log"
    print("--- パスの構築 ---")
    print(f"  base       = {base}")
    print(f"  log_path   = {log_path}")
    print(f"  parts      = {log_path.parts}")  # tuple に分解
    print(f"  parent     = {log_path.parent}")
    print(f"  name       = {log_path.name}")     # ファイル名
    print(f"  stem       = {log_path.stem}")     # 拡張子なし
    print(f"  suffix     = {log_path.suffix}")   # 拡張子
    print(f"  with_suffix('.gz') = {log_path.with_suffix('.gz')}")

    # ============================================================
    # カレントディレクトリ・ホーム・絶対パス
    # ============================================================
    print("\n--- 特殊なパス ---")
    print(f"  Path.cwd()   = {Path.cwd()}")
    print(f"  Path.home()  = {Path.home()}")
    rel = Path("foo/bar.txt")
    print(f"  rel.is_absolute() = {rel.is_absolute()}")
    print(f"  rel.resolve()     = {rel.resolve()}  # 絶対パス化（存在しなくてもよい）")

    # ============================================================
    # 存在チェックと読み書き
    # ============================================================
    # tempfile を使ってその場で作って試す。
    #
    # tempfile.TemporaryDirectory は **本物のディレクトリを実際にディスクに作る**
    # API（例: /var/folders/.../tmpXXXXXX）。削除処理を書いていないように見えるのは、
    # with（context manager）の終了時に **中身ごと再帰削除** されるため。
    # 明示的に書くと次の try/finally と等価:
    #
    #   import shutil
    #   tmpdir = tempfile.mkdtemp()
    #   try:
    #       ...
    #   finally:
    #       shutil.rmtree(tmpdir)
    #
    # 「リソースの取得と解放を with に括り付ける」context manager の典型例。
    # 詳しくは samples/08_context_managers_with.py を参照。
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        target = tmp / "hello.txt"
        target.write_text("こんにちは\n世界\n", encoding="utf-8")

        print("\n--- 読み書き ---")
        print(f"  exists       = {target.exists()}")
        print(f"  is_file      = {target.is_file()}")
        print(f"  is_dir       = {target.is_dir()}")
        print(f"  size (bytes) = {target.stat().st_size}")
        print(f"  read_text    = {target.read_text(encoding='utf-8')!r}")

        # ディレクトリを再帰的に作る（mkdir -p に相当）
        nested = tmp / "a" / "b" / "c"
        nested.mkdir(parents=True, exist_ok=True)
        (nested / "x.txt").write_text("x", encoding="utf-8")
        (nested / "y.log").write_text("y", encoding="utf-8")
        (tmp / "top.md").write_text("# top", encoding="utf-8")

        # ============================================================
        # 走査: iterdir / glob / rglob
        # ============================================================
        print("\n--- iterdir (直下のみ) ---")
        for p in sorted(tmp.iterdir()):
            kind = "DIR " if p.is_dir() else "FILE"
            print(f"  {kind} {p.name}")

        print("\n--- glob('**/*.txt') (再帰) ---")
        for p in sorted(tmp.glob("**/*.txt")):
            # tmp からの相対パスを表示すると見やすい
            print(f"  {p.relative_to(tmp)}")

        print("\n--- rglob('*.log') (再帰の glob と同じ) ---")
        for p in sorted(tmp.rglob("*.log")):
            print(f"  {p.relative_to(tmp)}")


if __name__ == "__main__":
    main()
