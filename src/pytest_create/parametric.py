"""A Python module used for parameterizing Literal's and common types."""
import inspect
import itertools
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Any
from typing import Callable
from typing import Dict
from typing import FrozenSet
from typing import Generic
from typing import List
from typing import Literal
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import get_args
from typing import get_origin
from typing import get_type_hints

from pytest_create.type_sets import PREDEFINED_TYPE_SETS


T = TypeVar("T")
KT = TypeVar("KT")
VT = TypeVar("VT")


DEFAULT_SUM_TYPES: Set[Type] = {Union, Optional, Enum}
DEFAULT_PRODUCT_TYPES: Set[Type] = {
    List,
    list,
    Set,
    set,
    FrozenSet,
    frozenset,
    Dict,
    dict,
    Tuple,
    tuple,
}


@dataclass(frozen=True)
class ExpandedType(Generic[T]):
    """A dataclass used to represent a type with expanded type arguments."""

    primary_type: Type[T]
    type_args: Tuple[Union[Type, "ExpandedType"], ...]


@dataclass(frozen=True)
class Config:
    """A dataclass used to configure the expansion of types."""

    max_elements: int = 5
    max_depth: int = 5
    custom_handlers: Dict[
        Type, Callable[[Type[T], "Config"], Set[Union[T, ExpandedType]]]
    ] = field(default_factory=dict)


DEFAULT_CONFIG: Config = Config()


def return_self(arg: T, config: Config = None) -> T:
    """Returns the provided argument."""
    return {arg}


def expand_type(
    type_arg: Type[T], config: Config = DEFAULT_CONFIG
) -> Set[Union[Type, ExpandedType]]:
    """Expands the provided type into the set of all possible subtype combinations."""
    origin: Any = get_origin(type_arg) or type_arg

    if origin in PREDEFINED_TYPE_SETS:
        return {origin}

    type_handlers: Dict[
        Type, Callable[[Type[T], Config], Set[Union[T, ExpandedType]]]
    ] = {
        Literal: return_self,
        Ellipsis: return_self,
        **{sum_type: expand_sum_type for sum_type in DEFAULT_SUM_TYPES},
        **{product_type: expand_product_type for product_type in DEFAULT_PRODUCT_TYPES},
    }

    # Add custom handlers from configuration
    type_handlers.update(config.custom_handlers)

    if origin in type_handlers:
        return type_handlers[origin](type_arg, config)

    # Check if a custom class has type annotations
    if (
        inspect.isclass(type_arg)
        or inspect.isfunction(type_arg)
        or inspect.ismethod(type_arg)
        or inspect.ismodule(type_arg)
    ):
        type_hints: Dict[str, Type] = get_type_hints(type_arg)
        type_hints.pop("return", None)
        type_hint_sets: Set[Set[Union[T, ExpandedType]]] = {
            *itertools.product(
                expand_type(type_hint, config) for type_hint in type_hints.values()
            )
        }
        if type_hints:
            return {
                ExpandedType(type_arg, tuple(type_hint_set))
                for type_hint_set in type_hint_sets
            }
    return set()


def expand_sum_type(type_arg: Type[T], config: Config) -> Set[Union[T, ExpandedType]]:
    """Expands a sum type into the set of all possible subtype combinations."""
    return {
        x
        for x in itertools.chain.from_iterable(
            expand_type(arg, config) for arg in get_args(type_arg)
        )
    }


def expand_product_type(
    type_arg: Type[T], config: Config
) -> Set[Union[T, ExpandedType]]:
    """Expands a product type into the set of all possible subtype combinations."""
    origin: Any = get_origin(type_arg) or type_arg
    args: Tuple[Any, ...] = get_args(type_arg)
    sets: List[Set[Union[T, ExpandedType]]] = [expand_type(arg, config) for arg in args]
    product_sets: Tuple[Union[T, ExpandedType], ...] = tuple(itertools.product(*sets))
    return {ExpandedType(origin, tuple(product_set)) for product_set in product_sets}
