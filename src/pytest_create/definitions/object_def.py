"""A module used for rendering the source code of a Python object."""
from dataclasses import dataclass
from typing import TypeVar
from typing import Union

from loguru import logger

from pytest_create.definitions.docstring_def import DocstringDef
from pytest_create.definitions.render import TemplateRendered


T = TypeVar("T")


@dataclass
class ObjectDef(TemplateRendered):
    """Abstract base class for object definitions."""

    docstring: Union[None, DocstringDef, str] = None

    def __post_init__(self):
        """Initialize the object definition."""
        logger.debug(f"{self.__class__.__name__} - {self.name}")
        if isinstance(self.docstring, str):
            self.docstring: DocstringDef = DocstringDef.from_string(self.docstring)
        elif isinstance(self.docstring, DocstringDef):
            self.docstring: DocstringDef = self.docstring
        else:
            self.docstring: DocstringDef = DocstringDef(None)

    def __str__(self) -> str:
        """Return the rendered object definition."""
        return self.render()
