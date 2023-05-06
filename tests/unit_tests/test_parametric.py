from types import NoneType
from typing import Any
from typing import Dict
from typing import FrozenSet
from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

import pytest

from pytest_create.parametric import Config
from pytest_create.parametric import ExpandedType
from pytest_create.parametric import expand_type


T = TypeVar("T")


class DummyClass:
    pass


@pytest.mark.parametrize(
    argnames=["type_arg", "expected"],
    argvalues=[
        ((DummyClass), {DummyClass}),
    ],
)
def test_expand_type_with_non_supported_type(
    type_arg: Type[T], expected: Set[Type[T]]
) -> None:

    assert expand_type(type_arg) == expected


@pytest.mark.parametrize(
    argnames=["type_arg", "expected"],
    argvalues=[
        (int, {int}),
        (float, {float}),
        (complex, {complex}),
        (str, {str}),
        (bytes, {bytes}),
        (bool, {bool}),
        (type(None), {NoneType}),
    ],
)
def test_base_types(type_arg: Type[T], expected: Set[Type[T]]) -> None:

    assert expand_type(type_arg) == expected


@pytest.mark.parametrize(
    argnames=["type_arg", "expected"],
    argvalues=[
        (List[int], [ExpandedType(list, (int,))]),
        (List[List[int]], [ExpandedType(list, (ExpandedType(list, (int,)),))]),
        (Dict[str, int], [ExpandedType(dict, (str, int))]),
        (Dict[str, List[int]], [ExpandedType(dict, (str, ExpandedType(list, (int,))))]),
        (Tuple[int], [ExpandedType(tuple, (int,))]),
        (Tuple[int, str], [ExpandedType(tuple, (int, str))]),
        (Tuple[int, ...], [ExpandedType(tuple, (int, ...))]),
        (
            Tuple[int, Dict[str, int]],
            [ExpandedType(tuple, (int, ExpandedType(dict, (str, int))))],
        ),
        (
            Tuple[int, Union[float, str]],
            [ExpandedType(tuple, (int, float)), ExpandedType(tuple, (int, str))],
        ),
        (Set[str], [ExpandedType(set, (str,))]),
        (FrozenSet[str], [ExpandedType(frozenset, (str,))]),
    ],
    ids=lambda x: str(x),
)
def test_expand_type_with_product_types(
    type_arg: Type[T], expected: Sequence[Any]
) -> None:

    assert expand_type(type_arg) == {*expected}


@pytest.mark.parametrize(
    argnames=["type_arg", "expected"],
    argvalues=[
        (Union[int, str], [int, str]),
        (Union[int, str, float], [int, str, float]),
        (Literal["a", "b", "c"], [Literal["a", "b", "c"]]),
        (Optional[int], [int, NoneType]),
        (Optional[Optional[int]], [int, NoneType]),
        (Optional[Union[int, str]], [int, str, NoneType]),
    ],
    ids=lambda x: str(x),
)
def test_expand_type_with_sum_types(type_arg: Type[T], expected: Sequence[Any]) -> None:

    assert expand_type(type_arg) == {*expected}


@pytest.mark.parametrize(
    argnames=["type_arg", "expected"],
    argvalues=[
        (List[int], [ExpandedType(list, (int,))]),
        (List[List[int]], [ExpandedType(list, (ExpandedType(list, (int,)),))]),
        (Dict[str, int], [ExpandedType(dict, (str, int))]),
        (Dict[str, List[int]], [ExpandedType(dict, (str, ExpandedType(list, (int,))))]),
        (Tuple[int], [ExpandedType(tuple, (int,))]),
        (Tuple[int, str], [ExpandedType(tuple, (int, str))]),
        (Tuple[int, ...], [ExpandedType(tuple, (int, ...))]),
        (
            Tuple[int, Dict[str, int]],
            [ExpandedType(tuple, (int, ExpandedType(dict, (str, int))))],
        ),
    ],
    ids=lambda x: str(x),
)
def test_expand_type_with_recursive_types(
    type_arg: Type[T], expected: Sequence[Any]
) -> None:

    assert expand_type(type_arg) == {*expected}


@pytest.mark.parametrize(
    argnames=["type_arg", "expected"],
    argvalues=[
        (
            List[Union[str, int]],
            [ExpandedType(list, (str,)), ExpandedType(list, (int,))],
        ),
        (
            List[Union[str, int, float]],
            [
                ExpandedType(list, (str,)),
                ExpandedType(list, (int,)),
                ExpandedType(list, (float,)),
            ],
        ),
        (
            Union[List[str], List[int]],
            [ExpandedType(list, (str,)), ExpandedType(list, (int,))],
        ),
        (
            Union[List[str], List[int], List[float]],
            [
                ExpandedType(list, (str,)),
                ExpandedType(list, (int,)),
                ExpandedType(list, (float,)),
            ],
        ),
        (
            List[Union[Dict[str, int], Optional[int]]],
            [
                ExpandedType(list, (ExpandedType(dict, (str, int)),)),
                ExpandedType(list, (NoneType,)),
                ExpandedType(list, (int,)),
            ],
        ),
    ],
    ids=lambda x: str(x),
)
def test_expand_type_with_combinations(
    type_arg: Type[T], expected: Sequence[Any]
) -> None:
    assert expand_type(type_arg) == {*expected}


def test_optional_expansion() -> None:
    result: Set[Union[Any, ExpandedType[Any]]] = expand_type(Optional[int])
    assert NoneType in result
    assert int in result


def test_union_expansion() -> None:
    result: Set[Union[Any, ExpandedType[Any]]] = expand_type(Union[int, str])
    assert NoneType not in result
    assert int in result
    assert str in result


def test_expanded_type() -> None:
    result: Set[Union[Any, ExpandedType[Any]]] = expand_type(Dict[str, Optional[int]])
    assert ExpandedType(dict, (str, int)) in result
    assert ExpandedType(dict, (str, NoneType)) in result


def test_custom_handler() -> None:
    def custom_handler(
        type_arg: Type[T], config: Config
    ) -> Set[Union[Any, ExpandedType[T]]]:
        return {int}

    config: Config = Config(max_elements=5, custom_handlers={list: custom_handler})
    assert expand_type(List[str], config) == {int}
