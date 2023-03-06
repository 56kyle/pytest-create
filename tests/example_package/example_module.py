"""Example module for testing pytest-create."""
import importlib
from typing import TypeVar


example_variable: str = ""


def example_function() -> bool:
    """Example function."""
    return True


class ExampleClassA:
    """Example class."""

    def example_method(self) -> bool:
        """Example method."""
        return True


if __name__ == "__main__":  # pragma: no cover
    print(importlib)
    print(TypeVar)
