"""Example module for testing pytest-create."""
import importlib
from types import ModuleType
from types import coroutine
from typing import Generator
from typing import TypeVar
from typing import runtime_checkable


example_variable: str = ""


def example_function() -> bool:
    """Example function."""
    return True


class ExampleClass:
    """Example class."""

    def example_method(self) -> bool:
        """Example method."""
        return True


if __name__ == "__main__":
    print(importlib)
    print(ModuleType)
    print(coroutine)
    print(Generator)
    print(TypeVar)
    print(runtime_checkable)
