"""A module used for rendering the source code of a Python Class."""
import inspect
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import List
from typing import Union

from jinja2 import Template

from pytest_create.definitions.object_def import ObjectDef
from pytest_create.definitions.templates import CLASS_TEMPLATE


@dataclass
class ClassDef(ObjectDef):
    """A class used for rendering the source code of a Python Class."""

    # signature: Optional[inspect.Signature] = field(default_factory=inspect.Signature)
    bases: List[str] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)
    definitions: List[Union[ObjectDef, inspect.Parameter]] = field(default_factory=list)
    template: ClassVar[Template] = CLASS_TEMPLATE
