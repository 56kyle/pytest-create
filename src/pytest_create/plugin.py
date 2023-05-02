"""The pytest-create pytest plugin."""
import inspect
import itertools
from pathlib import Path
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

import pytest
from _pytest.python import Metafunc
from loguru import logger

from pytest_create.create import create_tests
from pytest_create.parametric import Config
from pytest_create.parametric import ExpandedType
from pytest_create.parametric import expand_type
from pytest_create.parametric import get_args


T = TypeVar("T")


def pytest_generate_tests(metafunc: Metafunc) -> None:
    """Generate parametrized tests for the given argnames and types in argvalues."""
    for marker in metafunc.definition.iter_markers(name="parametrize_types"):
        if len(marker.args) == 2:
            if inspect.isfunction(marker.args[1]):
                parametrize_function(metafunc, marker.args[1])
                continue
            if inspect.isclass(marker.args[1]):
                parametrize_class(metafunc, marker.args[1])
                continue
        parametrize_types(metafunc, *marker.args, **marker.kwargs)


def parametrize_types(
    metafunc: Metafunc,
    argnames: Union[str, Sequence[str]],
    types: Sequence[Type[T]],
    *,
    ids: Optional[Union[Sequence[str], Callable]] = None,
    **kwargs,
) -> None:
    """Parametrize a test function with the given types."""
    config: Config = Config(max_elements=5)

    type_expansions: List[Set[Union[Type[T], ExpandedType]]] = [
        expand_type(type_arg, config) for type_arg in types
    ]
    expansions_product: Set[Tuple[Union[Type[T], ExpandedType], ...]] = set(
        itertools.product(*type_expansions)
    )
    argvalues: List[Tuple[Union[Type[T], ExpandedType], ...]] = [
        tuple(expansion) for expansion in expansions_product
    ]

    if isinstance(ids, Sequence):
        ids: List[str] = [
            f"{original_id}-{type_arg}" for original_id in ids for type_arg in argvalues
        ]
    metafunc.parametrize(argnames=argnames, argvalues=argvalues, ids=ids, **kwargs)


def _expand_sets_of_types_into_cartesian_products(
    starting_types: Sequence[Union[Type[T], ExpandedType]]
) -> List[Tuple[Union[Type[T], ExpandedType], ...]]:
    """Expand a set of types into a list of tuples of types that have been expanded."""
    return [
        tuple(expansion)
        for expansion in set(
            itertools.product(*[expand_type(type_arg) for type_arg in starting_types])
        )
    ]


def parametrize_class(metafunc: Metafunc, class_type: Type[object]) -> None:
    """Parametrize a class using its constructor arguments."""
    class_args: Tuple[Union[Type[T], ExpandedType], ...] = get_args(class_type.__init__)
    argnames: List[str] = list(get_args(class_type.__init__))
    argvalues: List[
        Tuple[Union[Type[T], ExpandedType], ...]
    ] = _expand_sets_of_types_into_cartesian_products(class_args)
    metafunc.parametrize(
        argnames=argnames,
        argvalues=argvalues,
        ids=[f"{class_type.__name__}-{type_arg}" for type_arg in argvalues],
    )


def parametrize_function(metafunc: Metafunc, function: Callable[..., Any]) -> None:
    """Parametrize a function using its arguments."""
    function_args: Tuple[Union[Type[T], ExpandedType], ...] = get_args(function)
    argnames: List[str] = list(get_args(function))
    argvalues: List[
        Tuple[Union[Type[T], ExpandedType], ...]
    ] = _expand_sets_of_types_into_cartesian_products(function_args)
    metafunc.parametrize(
        argnames=argnames,
        argvalues=argvalues,
        ids=[f"{function.__name__}-{type_arg}" for type_arg in argvalues],
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    """Adds pytest-create plugin options to the pytest CLI."""
    logger.debug("pytest_addoption")
    group = parser.getgroup("Create")
    group.addoption(
        "--create",
        nargs="?",
        const=True,
        default=False,
        help="Create test files for a given package module.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Adds pytest-create plugin markers to the pytest CLI."""
    config.addinivalue_line(
        "markers",
        "parametrize_type(argnames, types, ids, *args, **kwargs):"
        " Generate parametrized tests for the given argnames and types in argvalues.",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: List[pytest.Item]
) -> None:
    """Creates new tests and skips existing tests when pytest-create is used."""
    logger.debug("pytest_collection_modifyitems")
    create: Union[str, bool, Tuple[str], Tuple[str, str], None] = config.getoption(
        "--create"
    )
    logger.debug(f"--create - {create}")
    if create not in [None, False]:
        src_path: Path = (
            Path(create).resolve()
            if isinstance(create, str)
            else _get_default_src(config)
        )
        dst_path: Path = (
            Path(config.args[0]).resolve()
            if config.args[0]
            else _get_default_dst(config)
        )
        create_tests(src=src_path, dst=dst_path)
        items.clear()


def _get_default_src(config: pytest.Config) -> Path:
    """Get the default source directory path."""
    logger.debug("_get_default_src")
    tests_dir: Optional[Path] = _get_tests_dir(config=config)
    if tests_dir is None:
        return Path.cwd()
    if is_in_tests_dir(Path.cwd()):
        return tests_dir.parent.parent
    return Path.cwd()


def _get_default_dst(config: pytest.Config) -> Path:
    """Get the default destination directory path.

    The default destination directory is assumed to be the tests/unit_tests/
    directory relative to the project root directory.
    """
    logger.debug("_get_default_dst")
    if is_in_tests_dir(config.rootpath):
        return config.rootpath
    tests_dir: Optional[Path] = _get_tests_dir(config=config)
    if tests_dir is None:
        return config.rootpath
    return tests_dir


def _get_tests_dir(config: pytest.Config) -> Optional[Path]:
    """Finds the tests directory and returns it."""
    resolved_root: Path = config.rootpath.resolve()
    if is_in_tests_dir(resolved_root):
        lower_case_path: Path = Path(*[part.lower() for part in resolved_root.parts])
        return Path(*resolved_root.parts[: lower_case_path.parts.index("tests") + 1])
    else:
        for path in resolved_root.glob("**/[Tt]ests"):
            return path
    return None


def is_in_tests_dir(path: Path) -> bool:
    """Returns true if "tests" is a part of the path."""
    return (
        "tests" in [part.lower() for part in path.parts]
        and path.stem.lower() != "tests"
    )
