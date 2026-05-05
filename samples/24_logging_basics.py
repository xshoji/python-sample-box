"""`logging` モジュールの基本作法。

`print` で済ませず logger を使う理由:

- ログレベル（DEBUG / INFO / WARNING / ERROR / CRITICAL）で出し分けできる
- 出力先（stdout / file / syslog 等）を後から差し替えられる
- フォーマット（時刻、モジュール名、レベル）を一元管理できる
- 例外を `logger.exception` でスタックトレース付きで残せる

慣習:

- 各モジュールの先頭で `logger = logging.getLogger(__name__)` を定義する
  → ロガー名がモジュール階層と一致し、出力フィルタや設定が効きやすい
- アプリのエントリポイント（main）で 1 回だけ `logging.basicConfig(...)` する
- ライブラリ側では basicConfig を呼ばない（呼び出し側の設定を上書きしてしまう）
"""

import logging


# モジュールごとに getLogger(__name__) するのが慣例。
# このファイルを直接実行すると __name__ は "__main__" になる。
logger = logging.getLogger(__name__)


def divide(a: float, b: float) -> float:
    logger.debug("divide called with a=%s, b=%s", a, b)
    try:
        return a / b
    except ZeroDivisionError:
        # logger.exception はスタックトレース付きで ERROR レベルとして記録する。
        # except 節の中でしか呼ばないこと（現在の例外情報を参照するため）。
        logger.exception("division by zero")
        return float("nan")


def main() -> None:
    # ============================================================
    # basicConfig: アプリのエントリポイントで一度だけ呼ぶ
    # ============================================================
    # - level     : この閾値より下のレベルは捨てる（DEBUG が一番細かい）
    # - format    : 出力 1 行のフォーマット。`%(...)s` は LogRecord 属性の埋め込み
    # - datefmt   : `%(asctime)s` の **時刻の形式** を別途指定するためのもの
    #
    # `%(name)s` の記法は Python の %-formatting:
    #
    #   "%(name)s" % {"name": "alice"}  → "alice"
    #
    # logging は各ログ 1 件を LogRecord にして dict 化し、format に流し込む。
    # よく使う LogRecord 属性:
    #
    #   %(asctime)s   時刻（人間可読、デフォルトは "2026-05-06 12:34:56,789"）
    #   %(levelname)s DEBUG / INFO / WARNING / ERROR / CRITICAL
    #   %(name)s      ロガー名（getLogger(__name__) で付けた名前）
    #   %(message)s   ログ本文（logger.info("...") の内容）
    #   %(filename)s  呼び出し元ファイル
    #   %(lineno)d    呼び出し元行番号
    #   %(funcName)s  呼び出し元関数名
    #
    # 全一覧: https://docs.python.org/ja/3/library/logging.html#logrecord-attributes
    #
    # asctime の形式を変えたければ datefmt を渡す:
    #   datefmt="%Y-%m-%dT%H:%M:%S"  # → "2026-05-06T12:34:56"
    #
    # なお、本文の方の引数渡し（logger.info("user=%s", name)）でも %-style を使う。
    # f-string で組むより、未出力時のコスト・例外時の堅牢性で有利。
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    print("--- レベル別の出力 ---")
    logger.debug("これは DEBUG（詳細トレース用）")
    logger.info("これは INFO（通常運用ログ）")
    logger.warning("これは WARNING（注意）")
    logger.error("これは ERROR（処理は続くが失敗）")
    logger.critical("これは CRITICAL（致命）")

    print("\n--- 引数の遅延評価（%-style） ---")
    user = "alice"
    count = 3
    # f-string ではなく `%s` プレースホルダを使うのが logging 慣習。
    # ログレベルで出力が抑制された場合、文字列構築コストも発生しない。
    logger.info("user=%s logged in (count=%d)", user, count)

    print("\n--- 例外と一緒に記録する ---")
    result = divide(10, 0)
    logger.info("divide result = %s", result)


if __name__ == "__main__":
    main()
