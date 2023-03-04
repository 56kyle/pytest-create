"""Example module for testing pytest-create."""
import importlib
from typing import TypeVar


example_variable_b: str = ""


def example_function_b() -> bool:
    """Example function."""
    return True


class ExampleClassB:
    """Example class B."""

    def example_method_b(self) -> bool:
        """Example method."""
        return True


if __name__ == "__main__":  # pragma: no cover
    print(importlib)
    print(TypeVar)
