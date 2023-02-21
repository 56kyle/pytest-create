from types import MethodType

from tests.example_package.example_module import ExampleClass
from tests.example_package.example_module import example_function
from tests.example_package.example_module import example_variable


def test_example_variable() -> None:
    """Tests the example_variable variable."""
    assert isinstance(example_variable, str)
    assert example_variable == ""


def test_example_function() -> None:
    """Tests the example_function function."""
    assert callable(example_function)
    assert example_function() is True


def test_example_class() -> None:
    """Tests the ExampleClass class."""
    assert isinstance(ExampleClass, type)
    assert ExampleClass()


def test_example_method() -> None:
    """Tests the example_method method."""
    assert isinstance(ExampleClass().example_method, MethodType)
    assert ExampleClass().example_method() is True
