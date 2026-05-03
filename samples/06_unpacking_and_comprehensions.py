"""unpacking と内包表記。

Python では「構造をほどく（unpacking）」と「小さな変換を式として書く（内包表記）」が頻出します。
このファイルではそれぞれ代表的なパターンを 1 つずつ動かしながら説明します。

Java / Go / TypeScript との対応:
- unpacking          : JS の destructuring `const [a, b] = arr;` に近い
- *rest unpacking    : JS の rest pattern `const [first, ...rest] = arr;` に近い
- list 内包表記       : Java Stream の `.filter().map().toList()` を 1 行で書く感覚
- dict 内包表記       : 同上だが結果が dict
"""


def main() -> None:
    # ====================================================================
    # 1. tuple unpacking（構造をほどいて複数の変数に同時代入）
    # ====================================================================
    # 右辺の tuple の要素数と、左辺の変数の数が一致していると、
    # 順番通りに変数へ代入される。Python では関数の複数戻り値もこの仕組みで受け取る。
    user = (1001, "alice", "admin")
    user_id, name, role = user
    # ↑ user_id = 1001, name = "alice", role = "admin" と同じこと
    print(f"user_id={user_id}, name={name}, role={role}")

    # ====================================================================
    # 2. *rest unpacking（要素数が可変な部分を 1 つの変数にまとめる）
    # ====================================================================
    # 変数名の頭に `*` を付けると、その変数は「残り全部を list で受け取る」になる。
    # `first` と `last` には先頭と末尾の 1 要素ずつ、`middle` には中間の要素全部が入る。
    # JavaScript の `const [first, ...middle, last] = arr;` と違い、
    # Python では rest を「真ん中」に置けるのが特徴。
    first, *middle, last = ["red", "green", "blue", "yellow"]
    # → first="red", middle=["green", "blue"], last="yellow"
    print(f"first={first}, middle={middle}, last={last}")

    # ====================================================================
    # 3. dict.items() で key と value を同時に取り出す
    # ====================================================================
    # dict をそのまま for で回すと「key だけ」が取れる。key と value の両方が
    # 欲しいときは .items() を呼ぶと (key, value) の tuple が順に返ってくる。
    # 後続の内包表記は、この .items() を使って key/value を同時に unpack している。
    scores = {"alice": 82, "bob": 59, "carol": 91}

    # ====================================================================
    # 4. リスト内包表記 + フィルタ条件
    # ====================================================================
    # 構造:  [<出力する式>  for <変数> in <iterable>  if <条件>]
    # 意味:  「scores の各 (name, score) について、score >= 80 のものだけ
    #        name を取り出して list を作る」
    # 同等の for ループに展開するとこう:
    #   passed_names = []
    #   for name, score in scores.items():
    #       if score >= 80:
    #           passed_names.append(name)
    passed_names = [name for name, score in scores.items() if score >= 80]
    # → ["alice", "carol"]   （bob は 59 なので除外）
    print(f"passed_names = {passed_names}")

    # ====================================================================
    # 5. 辞書内包表記 + 条件式（三項演算子）
    # ====================================================================
    # 構造:  {<key>: <value>  for <変数> in <iterable>}
    # ここでは value 側に Python の三項演算子 `A if 条件 else B` を埋め込み、
    # score が 80 以上なら "pass"、未満なら "retry" にラベル付けしている。
    # （三項演算子は Java/JS の `条件 ? A : B` と順序が違う点に注意）
    # 同等の for ループ:
    #   labels = {}
    #   for name, score in scores.items():
    #       labels[name] = "pass" if score >= 80 else "retry"
    labels = {name: ("pass" if score >= 80 else "retry") for name, score in scores.items()}
    # → {"alice": "pass", "bob": "retry", "carol": "pass"}
    print(f"labels = {labels}")

    # ====================================================================
    # 6. (key, value) の list から dict を作る
    # ====================================================================
    # 組み込みの dict() は (key, value) を要素に持つ iterable を受け取って
    # 辞書を組み立ててくれる。設定値や CSV 行を dict にまとめるときによく使う。
    # JS の `Object.fromEntries(pairs)` に相当。
    pairs = [("host", "localhost"), ("port", "8000")]
    config = dict(pairs)
    # → {"host": "localhost", "port": "8000"}
    print(f"config = {config}")


if __name__ == "__main__":
    main()
