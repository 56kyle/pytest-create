import os

import pytest

from pytest_create.definitions.class_def import ClassDef
from pytest_create.definitions.function_def import FunctionDef
from pytest_create.definitions.import_def import ImportDef
from pytest_create.definitions.module_def import ModuleDef


def test_module_def_init(module_def: ModuleDef) -> None:
    assert module_def


@pytest.mark.parametrize(
    argnames=["imports", "definitions"],
    argvalues=[
        (
            [ImportDef(module=os, obj=os.chdir)],
            [ClassDef(name="TestClass"), FunctionDef(name="test_function")],
        )
    ],
    ids=["os_chdir_import_and_class_and_function_definitions"],
    indirect=True,
)
def test_module_def_render(module_def: ModuleDef) -> None:
    rendered = module_def.render()

    expected = (
        "from os import chdir"
        "class TestClass:"
        "    pass"
        "def test_function():"
        "    pass"
    )
    assert rendered.replace("\n", "") == expected.replace("\n", "")
