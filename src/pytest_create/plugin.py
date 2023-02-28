"""The pytest-create pytest plugin."""
from pathlib import Path
from typing import List
from typing import Tuple
from typing import Union

import pytest
from loguru import logger

from pytest_create.create import create_tests


def pytest_addoption(parser: pytest.Parser):
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
    tests_dir: Path = _get_tests_dir(config=config)
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
    return _get_tests_dir(config=config)


def _get_tests_dir(config: pytest.Config) -> Path:
    resolved_root: Path = config.rootpath.resolve()
    if is_in_tests_dir(resolved_root):
        lower_case_path: Path = Path(*[part.lower() for part in resolved_root.parts])
        return Path(*resolved_root.parts[: lower_case_path.parts.index("tests") + 1])
    else:
        for path in resolved_root.glob("**/[Tt]ests"):
            return path


def is_in_tests_dir(path: Path) -> bool:
    """Returns true if "tests" is a part of the path."""
    return (
        "tests" in [part.lower() for part in path.parts]
        and path.stem.lower() != "tests"
    )
