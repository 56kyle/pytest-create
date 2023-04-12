import inspect
from typing import List
from typing import Union

import pytest

from pytest_create.definitions.class_def import ClassDef
from pytest_create.definitions.docstring_def import DocstringDef
from pytest_create.definitions.import_def import ImportDef
from pytest_create.definitions.module_def import ModuleDef
from pytest_create.definitions.object_def import ObjectDef


@pytest.fixture(params=["dummy_name"], ids=["dummy_name"])
def name(request: pytest.FixtureRequest) -> str:
    return getattr(request, "param", "dummy_name")


@pytest.fixture(params=[[]], ids=["no_decorators"])
def decorators(request: pytest.FixtureRequest) -> str:
    return getattr(request, "param", "@dummy_decorator")


@pytest.fixture(params=[[]], ids=["no_bases"])
def bases(request: pytest.FixtureRequest) -> List[str]:
    return getattr(request, "param", [])


@pytest.fixture(params=[""], ids=["empty_docstring"])
def docstring_def(request: pytest.FixtureRequest) -> DocstringDef:
    return DocstringDef(value=getattr(request, "param", ""))


@pytest.fixture(params=[[]], ids=["no_imports"])
def imports(request: pytest.FixtureRequest) -> List[ImportDef]:
    return getattr(request, "param", [])


@pytest.fixture(params=[[]], ids=["no_definitions"])
def definitions(request: pytest.FixtureRequest) -> List[ObjectDef]:
    return getattr(request, "param", [])


@pytest.fixture
def class_def(
    name: str,
    docstring_def: DocstringDef,
    bases: List[str],
    decorators: List[str],
    definitions: List[Union[ObjectDef, inspect.Parameter]],
) -> ClassDef:
    return ClassDef(
        name=name,
        docstring=docstring_def,
        bases=bases,
        decorators=decorators,
        definitions=definitions,
    )


@pytest.fixture
def module_def(
    name: str,
    docstring_def: DocstringDef,
    imports: List[ImportDef],
    definitions: List[ObjectDef],
) -> ModuleDef:
    return ModuleDef(
        name=name, docstring=docstring_def, imports=imports, definitions=definitions
    )
