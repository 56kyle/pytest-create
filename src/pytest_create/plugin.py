"""The pytest-create pytest plugin."""
import pytest

from pathlib import Path
from typing import List, Type, Literal, Sequence, Callable, Any
from typing import Optional
from typing import Tuple
from typing import Union

from loguru import logger
from _pytest.python import Metafunc

from pytest_create.parametric import SupportsParametrize, get_args, PREDEFINED_TYPE_LITERALS
from pytest_create.create import create_tests


from typing import Optional, List, Type, Union, Sequence, Callable


def pytest_generate_tests(metafunc: Metafunc) -> None:
    for marker in metafunc.definition.iter_markers(name="parametrize_type"):
        parametrize_types(metafunc, *marker.args, **marker.kwargs)


def parametrize_types(
    metafunc: Metafunc,
    argnames: Union[str, Sequence[str]],
    types: List[Type],
    ids: Optional[Union[Sequence[str], Callable]] = None,
    *args, **kwargs
) -> None:
    argvalues = []

    for arg_type in types:
        if isinstance(arg_type, SupportsParametrize):
            if arg_type in PREDEFINED_TYPE_LITERALS:
                argvalues.append(get_args(PREDEFINED_TYPE_LITERALS[arg_type]))
            elif getattr(arg_type, "__origin__", None) is Literal:
                argvalues.append(get_args(arg_type))

    if argnames and argvalues:
        metafunc.parametrize(argnames=argnames, argvalues=list(zip(*argvalues)), ids=ids, *args, **kwargs)


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
    config.addinivalue_line(
        "markers",
        "parametrize_type(argnames, argvalues): Generate parametrized tests for the given argnames and types in argvalues.",
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

