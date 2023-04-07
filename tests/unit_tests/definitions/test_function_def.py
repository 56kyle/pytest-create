import inspect

import pytest

from pytest_create.definitions.function_def import CLS_PARAMETER
from pytest_create.definitions.function_def import SELF_PARAMETER
from pytest_create.definitions.function_def import FunctionDef
from pytest_create.definitions.templates import FUNCTION_TEMPLATE


def test_function_def_init() -> None:
    f: FunctionDef = FunctionDef(name="test_function")
    assert f.name == "test_function"
    assert f.signature == inspect.Signature()
    assert f.code == "pass"
    assert f.decorators == []


def test_function_def_as_staticmethod() -> None:
    f: FunctionDef = FunctionDef.as_staticmethod(name="test_staticmethod")
    assert f.decorators is not None
    assert "@staticmethod" in f.decorators


def test_function_def_as_staticmethod_with_decorator_already_present() -> None:
    f: FunctionDef = FunctionDef.as_staticmethod(
        name="test_staticmethod", decorators=["@staticmethod"]
    )
    assert f.decorators is not None
    assert "@staticmethod" in f.decorators


def test_function_def_as_classmethod() -> None:
    f: FunctionDef = FunctionDef.as_classmethod(name="test_classmethod")
    assert f.decorators is not None
    assert "@classmethod" in f.decorators
    assert CLS_PARAMETER in f.signature.parameters.values()


def test_function_def_as_classmethod_with_decorator_already_present() -> None:
    f: FunctionDef = FunctionDef.as_classmethod(
        name="test_classmethod", decorators=["@classmethod"]
    )
    assert f.decorators is not None
    assert "@classmethod" in f.decorators
    assert CLS_PARAMETER in f.signature.parameters.values()


def test_function_def_as_classmethod_with_cls_already_present() -> None:
    f: FunctionDef = FunctionDef.as_classmethod(
        name="test_classmethod", signature=inspect.Signature(parameters=[CLS_PARAMETER])
    )
    assert CLS_PARAMETER in f.signature.parameters.values()


def test_function_def_as_classmethod_with_cls_not_present() -> None:
    f: FunctionDef = FunctionDef.as_classmethod(name="test_classmethod")
    assert CLS_PARAMETER in f.signature.parameters.values()


def test_function_def_as_method() -> None:
    f: FunctionDef = FunctionDef.as_method(name="test_method")
    assert SELF_PARAMETER in f.signature.parameters.values()


def test_function_def_as_method_with_self_already_present() -> None:
    f: FunctionDef = FunctionDef.as_method(
        name="test_method", signature=inspect.Signature(parameters=[SELF_PARAMETER])
    )
    assert SELF_PARAMETER in f.signature.parameters.values()


def test_function_def_as_method_with_self_not_present() -> None:
    f: FunctionDef = FunctionDef.as_method(name="test_method")
    assert SELF_PARAMETER in f.signature.parameters.values()


@pytest.fixture
def example_function_def() -> FunctionDef:
    return FunctionDef(
        name="test_function", code="print('Hello World')", decorators=["@staticmethod"]
    )


def test_function_def_render(example_function_def: FunctionDef) -> None:
    rendered = example_function_def.render()

    expected = FUNCTION_TEMPLATE.render(
        name="test_function",
        signature=inspect.Signature(),
        code="print('Hello World')",
        decorators=["@staticmethod"],
        indent_width=4,
        docstring="",
    )

    assert rendered.strip() == expected.strip()
