# 19_init_py_and_packages

Python の **`__init__.py`** と **package** の仕組みを、実際に動かしながら確認するサンプルです。

## `__init__.py` とは

ある「ディレクトリ」を Python の package として扱うための入口ファイルです。次のような役割があります。

1. **package である印**
   そのディレクトリが「package」として認識されるためのマーカー。Python 3.3+ では無くても *namespace package* として認識されますが、ふつうの package では明示的に置きます。

2. **package の初期化コードの置き場**
   `import mypkg` などで package が **最初にロードされたタイミングで 1 度だけ** 実行されます。`sys.modules` にキャッシュされるため、何度 import しても再実行されません。

3. **公開 API のキュレーション**
   内部モジュールで定義したクラスや関数を `__init__.py` に再 import しておくことで、`mypkg.Greeter` のようにフラットに使わせられます。利用者は内部の物理構成を意識せずに済みます。

4. **メタ情報の置き場**
   `__version__`、`__author__`、`__all__` などをここで定義するのが慣例です。

## ディレクトリ構成

```
samples/19_init_py_and_packages/
    main.py                  # エントリポイント
    mypkg/
        __init__.py          # package の入口。初期化 + 公開 API curation
        core.py              # 公開クラス・関数
        helpers.py           # __init__.py 経由では公開していない内部用
        sub/
            __init__.py      # サブ package の入口
            deep.py          # ネストしたモジュール
```

## 動かし方

このサンプルは標準ライブラリだけで動きます。

```bash
python samples/19_init_py_and_packages/main.py
```

スクリプト実行時、Python はスクリプトの置かれているディレクトリを `sys.path[0]` に自動で入れるため、追加設定なしで `import mypkg` が解決できます。

## 観察できるポイント

`main.py` は次の 7 点を順に確認します。

1. **初回 import 時に `__init__.py` が走る**
   `[mypkg] __init__.py が実行されました` のメッセージが出るのは初回だけ。
2. **2 回目以降は再実行されない**
   `sys.modules['mypkg']` にキャッシュ済み。
3. **再エクスポートによるフラットアクセス**
   `__init__.py` で `from .core import Greeter, greet` しているので、利用者は `mypkg.core` を知らなくてよい。
4. **`__all__` の効き方**
   `__all__` は `from mypkg import *` の対象を制御するだけ。アクセス制御ではない。
5. **「公開していない」内部モジュールにも直接アクセスできてしまう**
   `from mypkg.helpers import internal_helper` は通る。Python に真のプライベートは無く、慣習で守るしかない。
6. **サブ package も自分の `__init__.py` を持てる**
   `mypkg.sub` を初めて触ったときに `mypkg/sub/__init__.py` が走る。
7. **package もモジュールオブジェクトの一種**
   `mypkg.__file__` / `mypkg.__path__` で実体の場所が分かる。

## 他言語との対応

- **Java**: `package` 宣言と物理ディレクトリが一致するだけで、Python のような「package 初期化ファイル」は存在しません。
- **Go**: 同じディレクトリ内の `.go` ファイルが暗黙に同じ package。`init()` 関数が初期化コードを書く場所で、Python の `__init__.py` に役割が近いです。
- **Node.js**: `index.js`（CommonJS）が、ディレクトリを `require`/`import` したときの入口として機能する点で似ています。

## 知っておくと得する補足

### namespace package（PEP 420）

Python 3.3 以降は、`__init__.py` の **無いディレクトリ** も「namespace package」として import できます。複数の場所に分散したサブ package をまとめたいケース（巨大 OSS や分割配布）で使われます。日常的なアプリ開発ではあまり意識せず、明示的な `__init__.py` を書くのが無難です。

### 重い初期化を `__init__.py` に書かない

`__init__.py` は package の利用者が import するたびに（事実上）必ず走る入口です。DB 接続・ネットワーク I/O・大量のファイル読み込みのような重い処理を入れると、import コスト全体が膨らみます。**重い初期化は別関数 / 別モジュールに切り出して、必要なときだけ呼ぶ** のが定石です。

### `__init__.py` を空にしておくケースも普通

「特に再エクスポートしたいものが無く、初期化コードも要らない」場合は、空の `__init__.py` を置いておくだけで充分です。明示性のためだけに空ファイルを置く運用は普通にあります。
