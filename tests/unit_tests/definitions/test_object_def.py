from dataclasses import dataclass
from typing import ClassVar
from typing import Union

from jinja2 import Template

from pytest_create.definitions.object_def import DocstringDef
from pytest_create.definitions.object_def import ObjectDef


@dataclass
class MockObjectDef(ObjectDef):
    docstring: Union[None, str, DocstringDef] = DocstringDef("This is a mock object.")
    template: ClassVar[Template] = Template("{{ value }}")


def test_object_def_post_init_str_docstring():
    obj = MockObjectDef(name="mock", docstring="This is a mock object.")
    assert obj.name == "mock"
    assert obj.docstring.value == "This is a mock object."


def test_object_def_post_init_docstring_def():
    docstring = DocstringDef(value="This is a mock object.")
    obj = MockObjectDef(name="mock", docstring=docstring)
    assert obj.name == "mock"
    assert obj.docstring.value == "This is a mock object."


def test_object_def_post_init_no_docstring():
    obj = MockObjectDef(name="mock", docstring=None)
    assert obj.name == "mock"
    assert obj.docstring.value == ""


def test_object_def_str():
    obj = MockObjectDef(name="mock")
    assert isinstance(str(obj), str)
