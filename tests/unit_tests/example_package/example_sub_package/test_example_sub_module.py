from types import MethodType

from tests.example_package.example_sub_package.example_sub_module import ExampleClassB
from tests.example_package.example_sub_package.example_sub_module import (
    example_function_b,
)
from tests.example_package.example_sub_package.example_sub_module import (
    example_variable_b,
)


def test_example_variable_b() -> None:
    """Tests the example_variable_b variable."""
    assert isinstance(example_variable_b, str)
    assert example_variable_b == ""


def test_example_function() -> None:
    """Tests the example_function function."""
    assert callable(example_function_b)
    assert example_function_b() is True


def test_example_class() -> None:
    """Tests the ExampleClassA class."""
    assert isinstance(ExampleClassB, type)
    assert ExampleClassB()


def test_example_method() -> None:
    """Tests the example_method method."""
    assert isinstance(ExampleClassB().example_method_b, MethodType)
    assert ExampleClassB().example_method_b() is True
