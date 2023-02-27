"""The pytest-create pytest plugin."""
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

import pytest
from loguru import logger

from pytest_create.create import create_tests


def pytest_addoption(parser):
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
    group.addoption(
        "--src",
        type=str,
        default=None,
        help="Path to the package module to create test files for.",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: List[pytest.Item]
) -> None:
    """Creates new tests and skips existing tests when pytest-create is used."""
    logger.debug("pytest_collection_modifyitems")
    create: Union[str, bool, None] = config.getoption("--create")
    if create not in [None, False]:
        src: Optional[str] = config.getoption(name="--src")
        if isinstance(create, str):
            src = create if src is None else src
        src_path: Path = Path(src).resolve() if src else _get_default_src(config)
        create_tests(src=src_path, dst=config.rootpath)
        items.clear()


def _get_default_src(config: pytest.Config) -> Path:
    """Get the default source directory path."""
    logger.debug("_get_default_src")
    logger.debug(f"config.rootpath - {config.rootpath}")
    logger.debug(f"cwd - {Path.cwd()}")
    conftest_file: Path = Path(__file__).resolve()
    logger.debug(f"conftest_file - {conftest_file}")

    return conftest_file.parent.parent / "src" / conftest_file.parent.name


def _get_default_dst(config: pytest.Config, src: Path) -> Path:
    """Get the default destination directory path.

    The default destination directory is assumed to be the tests/unit_tests/
    directory relative to the project root directory.
    """
    logger.debug("_get_default_dst")
    if is_in_tests_dir(config.rootpath):
        pass
    tests_dir = Path(__file__).resolve().parent.parent / "tests" / "unit_tests"
    src_relpath = src.relative_to(config.rootpath)
    return tests_dir / src_relpath


def is_in_tests_dir(path: Path) -> bool:
    """Returns true if "tests" is a part of the path."""
    return "tests" in [part.lower() for part in path.parts]
