"""A module used for rendering Python objects as source code."""
from dataclasses import dataclass
from dataclasses import fields
from pathlib import Path
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import MutableMapping
from typing import MutableSequence
from typing import Protocol
from typing import TypeVar
from typing import Union
from typing import runtime_checkable

from jinja2 import Template
from loguru import logger


T = TypeVar("T", covariant=True)
templates: Path = Path(__file__).parent / "templates"


@runtime_checkable
class SupportsRender(Protocol):
    """Supports render."""

    __slots__ = ()

    def render(self) -> str:
        """Makes sure that the object can be rendered."""
        pass


@dataclass
class TemplateRendered:
    """A class used for rendering Python objects using Jinja2 templates."""

    name: str
    indent_width: int = 4
    template: ClassVar[Template]

    def __dict__(self) -> Dict[str, Any]:
        """Returns a dictionary of the object's attributes."""
        non_rendered_dict: Dict[str, Any] = {}
        for _field in fields(self):
            non_rendered_dict[_field.name] = getattr(self, _field.name)
        return non_rendered_dict

    def render(self) -> str:
        """Renders the Python source code using a Jinja2 template."""
        logger.debug(f"render - {self.name}")
        return self.template.render(self._rendered_dict())

    def _rendered_dict(self) -> Dict[str, Any]:
        non_rendered_dict: Dict[str, Any] = self.__dict__()
        return self._recurse_render(non_rendered_dict)

    @classmethod
    def _recurse_render(
        cls, obj: T
    ) -> Union[str, T, MutableMapping[str, T], MutableSequence[T]]:
        if isinstance(obj, SupportsRender):
            return obj.render()
        if isinstance(obj, MutableMapping):
            return {k: cls._recurse_render(v) for k, v in obj.items()}
        if isinstance(obj, MutableSequence):
            return [cls._recurse_render(v) for v in obj]
        return obj
