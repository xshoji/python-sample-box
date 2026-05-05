"""`datetime` と `zoneinfo`: naive と aware の使い分け。

Python の `datetime` には 2 種類ある:

- **naive**: `tzinfo` を持たない datetime。「いつのどこの時刻か」が曖昧。
- **aware**: `tzinfo` を持つ datetime。明確に瞬間（instant）を表す。

業務で必ず踏む地雷:

- `datetime.now()` は naive を返す（ローカル時刻だが、tz 情報が付いていない）
- naive と aware を比較・演算すると `TypeError`
- DB / API 境界では UTC の aware で扱い、表示直前にローカルタイムへ変換するのが定石

3.9+ で標準ライブラリに `zoneinfo` が入り、3rd party (`pytz`) なしで IANA タイムゾーンを扱える。
"""

from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo


def main() -> None:
    # ============================================================
    # naive vs aware
    # ============================================================
    naive = datetime.now()                     # tzinfo を持たない
    aware_utc = datetime.now(tz=UTC)           # 3.11+: datetime.UTC が使える
    aware_tokyo = datetime.now(tz=ZoneInfo("Asia/Tokyo"))

    print("--- naive vs aware ---")
    print(f"  naive       = {naive}        tzinfo={naive.tzinfo}")
    print(f"  aware (UTC) = {aware_utc}    tzinfo={aware_utc.tzinfo}")
    print(f"  aware (TYO) = {aware_tokyo}  tzinfo={aware_tokyo.tzinfo}")

    # ============================================================
    # naive と aware は混ぜられない
    # ============================================================
    print("\n--- naive と aware の比較は TypeError ---")
    try:
        _ = naive < aware_utc
    except TypeError as e:
        print(f"  TypeError: {e}")

    # ============================================================
    # タイムゾーン変換: astimezone
    # ============================================================
    # 同じ瞬間（instant）を、別のタイムゾーン表現に切り替える。
    # 「時刻の値」を変えるのではなく「どのタイムゾーンで表示するか」を切り替える。
    instant = datetime(2026, 5, 6, 12, 0, 0, tzinfo=UTC)
    print("\n--- astimezone で表示タイムゾーンを切り替える ---")
    print(f"  UTC   : {instant}")
    print(f"  Tokyo : {instant.astimezone(ZoneInfo('Asia/Tokyo'))}")
    print(f"  NY    : {instant.astimezone(ZoneInfo('America/New_York'))}")

    # ============================================================
    # naive を aware に「持ち上げる」
    # ============================================================
    # 既に「東京時刻と分かっている naive」を aware にしたいとき。
    # astimezone ではなく replace(tzinfo=...) を使う。
    # （astimezone は naive を「ローカルタイム」として解釈してしまうので別の意味になる）
    naive_tokyo = datetime(2026, 5, 6, 21, 0, 0)  # 東京の 21:00 という前提
    aware_from_naive = naive_tokyo.replace(tzinfo=ZoneInfo("Asia/Tokyo"))
    print("\n--- naive -> aware の付与 ---")
    print(f"  naive_tokyo       = {naive_tokyo}")
    print(f"  aware_from_naive  = {aware_from_naive}")
    print(f"  ↑ を UTC に直すと : {aware_from_naive.astimezone(UTC)}")

    # ============================================================
    # timedelta: 時間の差・加算
    # ============================================================
    print("\n--- timedelta ---")
    later = aware_utc + timedelta(days=1, hours=3)
    diff = later - aware_utc
    print(f"  aware_utc + 1日3時間 = {later}")
    print(f"  diff                  = {diff}  (total_seconds={diff.total_seconds()})")

    # ============================================================
    # ISO 8601 文字列とのやり取り
    # ============================================================
    # API / JSON 境界では文字列との往復が頻出。
    # - isoformat() : ISO 8601 文字列に変換
    # - fromisoformat(): 逆方向
    print("\n--- ISO 8601 文字列 ---")
    s = aware_utc.isoformat()
    print(f"  isoformat()           = {s}")
    parsed = datetime.fromisoformat(s)
    print(f"  fromisoformat(s)      = {parsed}")
    print(f"  parsed == aware_utc   -> {parsed == aware_utc}")


if __name__ == "__main__":
    main()
