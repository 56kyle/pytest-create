from dataclasses import dataclass
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import MutableMapping
from typing import MutableSequence
from typing import Union

import pytest
from jinja2 import Template

from pytest_create.definitions.render import SupportsRender
from pytest_create.definitions.render import TemplateRendered


@dataclass
class MockTemplateRendered(TemplateRendered):
    template: ClassVar[Template] = Template("{{ name }}")


@dataclass
class MockSupportsRender(SupportsRender):
    def render(self) -> str:
        return "rendered"


class MockSupportsRenderForTesting(SupportsRender):
    def render(self) -> str:
        return SupportsRender.render(self)


def test_supports_render_render() -> None:
    obj: MockSupportsRenderForTesting = MockSupportsRenderForTesting()
    obj.render()


def test_template_rendered_render() -> None:
    obj: MockTemplateRendered = MockTemplateRendered(name="mock")
    assert obj.render() == "mock"


def test_template_rendered_as_dict() -> None:
    obj: MockTemplateRendered = MockTemplateRendered(name="mock")
    assert obj.as_dict() == {"indent_width": 4, "name": "mock"}


@pytest.mark.parametrize(
    "value, expected",
    argvalues=[
        (MockSupportsRender(), "rendered"),
        ({"key": MockSupportsRender()}, {"key": "rendered"}),
        ([MockSupportsRender()], ["rendered"]),
        ("string", "string"),
    ],
    ids=["MockSupportsRender", "dict", "list", "str"],
)
def test_template_rendered_recurse_render(value: Any, expected: Any) -> None:
    obj: MockTemplateRendered = MockTemplateRendered(name="mock")
    result: Union[
        str,
        Dict[Any, Any],
        SupportsRender,
        MutableMapping[Any, MockTemplateRendered],
        MutableSequence[Dict[Any, Any]],
    ] = obj._recurse_render(value)
    assert result == expected


def test_template_rendered_rendered_dict() -> None:
    obj = MockTemplateRendered(name="mock")
    result: Union[
        str,
        Dict[Any, Any],
        SupportsRender,
        MutableMapping[Any, MockTemplateRendered],
        MutableSequence[Dict[Any, Any]],
    ] = obj._rendered_dict()
    assert result == {"indent_width": 4, "name": "mock"}
