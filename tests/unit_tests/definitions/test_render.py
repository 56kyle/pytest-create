from dataclasses import dataclass
from typing import ClassVar

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
    def render(self):
        super().render()


def test_supports_render_render():
    obj = MockSupportsRenderForTesting()
    obj.render()


def test_template_rendered_render():
    obj = MockTemplateRendered(name="mock")
    assert obj.render() == "mock"


def test_template_rendered_dict():
    obj = MockTemplateRendered(name="mock")
    assert obj.__dict__() == {"indent_width": 4, "name": "mock"}


def test_template_rendered_recurse_render():
    obj = MockTemplateRendered(name="mock")
    result = obj._recurse_render(MockSupportsRender())
    assert result == "rendered"

    result = obj._recurse_render({"key": MockSupportsRender()})
    assert result == {"key": "rendered"}

    result = obj._recurse_render([MockSupportsRender()])
    assert result == ["rendered"]

    result = obj._recurse_render("string")
    assert result == "string"


def test_template_rendered_rendered_dict():
    obj = MockTemplateRendered(name="mock")
    result = obj._rendered_dict()
    assert result == {"indent_width": 4, "name": "mock"}
