"""03_main_guard_and_imports.py から import される補助モジュール。"""

print("supporting_module_for_import.py was imported")


def greet(name: str) -> str:
    return f"hello, {name}"
