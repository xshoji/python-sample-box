"""mypkg.sub サブパッケージの `__init__.py`。

サブパッケージにも個別の `__init__.py` を置ける。トップの `mypkg/__init__.py` とは
別タイミング — `mypkg.sub` を最初に import したとき — に実行される。
"""

print("[mypkg.sub] __init__.py が実行されました")
