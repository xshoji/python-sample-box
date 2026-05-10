"""ファイル操作の実務入口: `pathlib`、`shutil`、`tempfile`、`os.walk`。

`pathlib.Path` はパス表現、`shutil` はコピー・削除などの高水準ファイル操作、
`tempfile` は一時ファイル / 一時ディレクトリを安全に作るために使う。
Java の `Path` / `Files` に近い役割を、Python 標準ライブラリでは複数モジュールで分担する。
"""

import os
import shutil
import tempfile
from pathlib import Path


def show_tree(root: Path) -> None:
    for current, dirs, files in os.walk(root):
        dirs.sort()
        files.sort()
        indent = "  " * len(Path(current).relative_to(root).parts)
        print(f"{indent}{Path(current).name}/")
        for file_name in files:
            print(f"{indent}  {file_name}")


def main() -> None:
    print("--- tempfile.TemporaryDirectory は終了時に自動削除される ---")
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        source = workdir / "source"
        backup = workdir / "backup"
        source.mkdir()

        report = source / "report.txt"
        report.write_text("売上レポート\n", encoding="utf-8")
        (source / "memo.txt").write_text("一時メモ\n", encoding="utf-8")

        print(f"一時ディレクトリ: {workdir}")
        print("\n--- shutil.copy2 でファイルをコピー ---")
        copied_report = workdir / "report-copy.txt"
        # shutil.copy2() は、ファイル内容だけでなく更新時刻などの metadata も
        # できるだけ保持してコピーする。Java の Files.copy(..., COPY_ATTRIBUTES) に近い。
        #
        # 名前の `2` は少し分かりづらいが、`copy()` の拡張版 / version 2 のような歴史的な名前。
        # 内容だけでよいなら copyfile()、権限 mode 程度までなら copy()、
        # backup / mirror のように属性もなるべく残したいなら copy2() を使う、という感覚。
        shutil.copy2(report, copied_report)
        print(copied_report.read_text(encoding="utf-8").strip())

        print("\n--- shutil.copytree でディレクトリごとコピー ---")
        shutil.copytree(source, backup)
        show_tree(workdir)

        print("\n--- shutil.rmtree でディレクトリごと削除 ---")
        shutil.rmtree(backup)
        show_tree(workdir)

    print("\nwith ブロックを抜けると、一時ディレクトリ全体が削除される")


if __name__ == "__main__":
    main()
