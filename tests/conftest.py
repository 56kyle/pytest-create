"""Pytest configuration file."""
import pathlib

import pytest


pytest_plugins = ["pytester", "pytest_create.plugin"]


@pytest.fixture(scope="session")
def tests_dir() -> pathlib.Path:
    """Returns the path to the tests directory."""
    return pathlib.Path(__file__).parent


@pytest.fixture(scope="session")
def example_package_dir(tests_dir: pathlib.Path) -> pathlib.Path:
    """Returns the path to the example package directory."""
    return tests_dir / "example_package"
