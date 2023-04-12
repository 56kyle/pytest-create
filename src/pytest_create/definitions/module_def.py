"""A module used for rendering the source code of a Python Module."""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import List

from jinja2 import Template

from pytest_create.definitions.import_def import ImportDef
from pytest_create.definitions.object_def import ObjectDef
from pytest_create.definitions.templates import MODULE_TEMPLATE


@dataclass
class ModuleDef(ObjectDef):
    """A class used for rendering the source code of a Python Module."""

    imports: List[ImportDef] = field(default_factory=list)
    definitions: List[ObjectDef] = field(default_factory=list)
    template: ClassVar[Template] = MODULE_TEMPLATE
