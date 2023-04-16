"""A Python module used for parameterizing Literal's and common types"""

import inspect
import pytest
import sys

from abc import ABCMeta
from dataclasses import dataclass
from _pytest.mark.structures import _ParametrizeMarkDecorator, ParameterSet
from typing import Type, TypeVar, get_args, Literal, Any, Union, Callable, Sequence, Set, Tuple, Iterable, Optional

# Predefined Literals for common built-in types
BoolLiteral = Literal[False, True]
IntLiteral = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
StrLiteral = Literal["", "a", "b", "c", "1", "2", "3", "example"]

# Predefined type-to-literal mapping
PREDEFINED_TYPE_LITERALS = {
    bool: BoolLiteral,
    int: IntLiteral,
    str: StrLiteral,
}


class SupportsParametrizeMeta(ABCMeta):
    def __instancecheck__(self, instance: Any) -> bool:
        # We check if the given instance is a Type or a Literal
        if not isinstance(instance, type) and not hasattr(instance, "__origin__"):
            return False

        # Check if the given instance is a Type[Literal]
        if getattr(instance, "__origin__", None) is Literal:
            return True

        # Check if the given instance is in the predefined type-to-literal mapping
        if instance in PREDEFINED_TYPE_LITERALS:
            return True

        return False


class SupportsParametrize(metaclass=SupportsParametrizeMeta):
    pass


@dataclass
class ParametricCall:
    argnames: Union[str, Sequence[str]]
    argvalues: Iterable[Union[ParameterSet, Sequence[object], object]]
    ids: Optional[
        Union[
            Iterable[Union[None, str, float, int, bool]],
            Callable[[Any], Optional[object]],
        ]
    ]


def get_parametric_decorators(obj: Callable[..., Any]) -> Set[_ParametrizeMarkDecorator]:


if __name__ == '__main__':
    # Test cases
    print(isinstance(bool, SupportsParametrize))
    print(isinstance(Literal[False, True], SupportsParametrize))
    print(not isinstance(True, SupportsParametrize))
    print(not isinstance("example", SupportsParametrize))






