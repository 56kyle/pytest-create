"""A module for the FunctionDef class."""
import inspect
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar
from typing import List
from typing import Optional

from jinja2 import Template

from pytest_create.definitions.object_def import ObjectDef
from pytest_create.definitions.templates import FUNCTION_TEMPLATE


CLS_PARAMETER: inspect.Parameter = inspect.Parameter(
    "cls", inspect.Parameter.POSITIONAL_OR_KEYWORD
)
SELF_PARAMETER: inspect.Parameter = inspect.Parameter(
    "self", inspect.Parameter.POSITIONAL_OR_KEYWORD
)


@dataclass
class FunctionDef(ObjectDef):
    """A class used for rendering the source code of a Python Function."""

    signature: inspect.Signature = field(default_factory=inspect.Signature)
    code: Optional[str] = field(default="pass")
    decorators: Optional[List[str]] = field(default_factory=list)
    template: ClassVar[Template] = FUNCTION_TEMPLATE

    def __post_init__(self):
        """Post init method for the FunctionDef class."""
        super().__post_init__()
        self.code: str = self.code if self.code else "pass"
        self.decorators: List[str] = (
            self.decorators if self.decorators is not None else []
        )

    @classmethod
    def as_staticmethod(cls, **kwargs):
        """Return a FunctionDef as a staticmethod."""
        function_def: FunctionDef = cls(**kwargs)
        if "@staticmethod" not in function_def.decorators:
            function_def.decorators.append("@staticmethod")
        return function_def

    @classmethod
    def as_classmethod(cls, **kwargs) -> "FunctionDef":
        """Return a FunctionDef as a classmethod."""
        function_def: FunctionDef = cls(**kwargs)
        if "@classmethod" not in function_def.decorators:
            function_def.decorators.append("@classmethod")
        if function_def.signature.parameters.get("cls", None) is None:
            function_def.signature = function_def.signature.replace(
                parameters=[CLS_PARAMETER, *function_def.signature.parameters]
            )
        return function_def

    @classmethod
    def as_method(cls, **kwargs) -> "FunctionDef":
        """Return a FunctionDef as a method."""
        function_def: FunctionDef = cls(**kwargs)
        if function_def.signature.parameters.get("self", None) is None:
            function_def.signature = function_def.signature.replace(
                parameters=[SELF_PARAMETER, *function_def.signature.parameters]
            )
        return function_def
