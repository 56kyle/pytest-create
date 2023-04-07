import os

import pytest

from pytest_create.definitions.class_def import ClassDef
from pytest_create.definitions.function_def import FunctionDef
from pytest_create.definitions.import_def import ImportDef
from pytest_create.definitions.module_def import ModuleDef


def test_module_def_init() -> None:
    module = ModuleDef(name="test_module")
    assert module.name == "test_module"
    assert module.definitions == []


@pytest.fixture
def example_module_def() -> ModuleDef:
    class_def = ClassDef(name="TestClass")
    function_def = FunctionDef(name="test_function")
    module = ModuleDef(
        name="test_module",
        definitions=[class_def, function_def],
        imports=[ImportDef(module=os, obj=os.chdir)],
    )
    return module


def test_module_def_render(example_module_def: ModuleDef) -> None:
    rendered = example_module_def.render()

    expected = (
        "from os import chdir"
        "class TestClass:"
        "    pass"
        "def test_function():"
        "    pass"
    )

    assert rendered.replace("\n", "") == expected.replace("\n", "")
