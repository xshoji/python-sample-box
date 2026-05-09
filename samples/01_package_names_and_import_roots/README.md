# 01_package_names_and_import_roots

Python における **ディレクトリ名・パッケージ名・import 探索起点** の関係を確認するサンプルです。

Java / PHP のように、ファイル先頭で次のような所属宣言を書く必要はありません。

```java
package com.example.app;
```

```php
namespace App\Services;
```

Python では、基本的に **ファイルを置いたディレクトリ構造** が import 名の階層になります。

## このサンプルの構成

```text
samples/01_package_names_and_import_roots/
    main.py
    app_like_package/
        __init__.py
        services/
            __init__.py
            mail.py
```

この構成では、`mail.py` は次の import 名で扱われます。

```python
import app_like_package.services.mail
```

`mail.py` の先頭に「自分は `app_like_package.services` に所属する」と書く必要はありません。

## Root はどこか

Python の import には、プロジェクト全体に固定された単一の Root があるわけではありません。

代わりに、`sys.path` に入っている各ディレクトリが import 探索の起点になります。

このサンプルを次のように実行すると:

```bash
python samples/01_package_names_and_import_roots/main.py
```

Python はスクリプトの置かれているディレクトリを `sys.path[0]` に入れます。

```text
samples/01_package_names_and_import_roots/  ← 探索起点
    app_like_package/
        services/
            mail.py
```

そのため、次の import が解決できます。

```python
from app_like_package.services import mail
```

## `src/` レイアウトの場合

実務では次のような `src/` レイアウトもよく使われます。

```text
project/
    pyproject.toml
    src/
        my_app/
            __init__.py
            services/
                __init__.py
                mail.py
```

この形にする場合、`pyproject.toml` などのプロジェクト設定で「パッケージは `src/` 配下から探す」と指定します。`pip install -e .` が常に `src/` を見に行くわけではありません。

例えば setuptools では、概念的には次のような設定で `src/` 配下を探索対象にします。

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

この場合の import 名は通常こうです。

```python
import my_app.services.mail
```

`src` は import 名の一部ではありません。

```python
# 普通はこうしない
import src.my_app.services.mail
```

`src/` は **パッケージそのものではなく、パッケージを置くための親ディレクトリ** です。

```text
project/src/my_app/services/mail.py
        ↑   ↑
        │   └─ import 名に入る package: my_app
        └───── import 探索の起点として使いたいディレクトリ
```

この構成で `import my_app.services.mail` を成功させるには、Python が `src/` の中を探せる必要があります。つまり、概念的には `src/` が `sys.path` 側に入っている必要があります。

開発時によく使う方法が、プロジェクトルートで実行する editable install です。

```bash
cd project
pip install -e .
```

`-e` は editable の意味で、「このプロジェクトを開発用にインストールする」指定です。どのディレクトリを package として扱うかは、`pyproject.toml` や `setup.py` などの設定で決まります。

`src/` レイアウトとして設定されているプロジェクトで editable install すると、ソースコードをコピーしてインストールするのではなく、作業中の `src/my_app/` を参照する形になります。そのため、`src/my_app/` のコードを編集すると、再インストールしなくても import される内容に反映されます。

要するに、`pip install -e .` は「このプロジェクトの package 設定を読んで、開発中のコードを import できるようにしておく」ための準備です。`src/` を見るのは、プロジェクトが `src/` レイアウトとして設定されている場合です。

## 19 番サンプルとの違い

このサンプルは、かなり初歩的な次の話に絞っています。

- ディレクトリ名が import 名になる
- Python では所属パッケージ宣言を書かない
- import の Root は `sys.path` の探索起点で決まる

`samples/19_init_py_and_packages/` では、その次の段階として `__init__.py` の実行タイミング、公開 API の整理、`__all__`、サブパッケージなどを扱います。

## 動かし方

```bash
python samples/01_package_names_and_import_roots/main.py
```
