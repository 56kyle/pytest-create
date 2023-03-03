import importlib.util
from importlib.machinery import ModuleSpec
from pathlib import Path

import pytest


@pytest.fixture(scope="function")
def example_module_spec(example_package_dir: Path) -> ModuleSpec:
    spec = importlib.util.spec_from_file_location(
        "example_module", example_package_dir / "example_module.py"
    )
    assert spec is not None
    assert spec.loader is not None
    return spec


@pytest.fixture
def config(pytester: pytest.Pytester) -> pytest.Config:
    tests_dir: Path = pytester.mkdir("tests")
    (tests_dir / "unit_tests").mkdir()
    config: pytest.Config = pytester.parseconfig()
    config._rootpath = tests_dir / "unit_tests"
    return config
