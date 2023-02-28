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


@pytest.fixture(scope="session")
def tmp_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root: Path = tmp_path_factory.mktemp("root")
    return root


@pytest.fixture(scope="session")
def tmp_src(tmp_root) -> Path:
    src: Path = tmp_root / "src"
    src.mkdir()
    (src / "__init__.py").touch()
    return src


@pytest.fixture(scope="session")
def tmp_tests(tmp_root: Path) -> Path:
    tests: Path = tmp_root / "tests"
    tests.mkdir()
    (tests / "__init__.py").touch()
    return tests


@pytest.fixture(scope="session")
def tmp_module(tmp_src: Path) -> Path:
    tmp_module: Path = tmp_src / "module.py"
    tmp_module.touch()
    return tmp_module


@pytest.fixture
def config(pytester: pytest.Pytester) -> pytest.Config:
    tests_dir: Path = pytester.mkdir("tests")
    (tests_dir / "unit_tests").mkdir()
    config: pytest.Config = pytester.parseconfig()
    config._rootpath = tests_dir / "unit_tests"
    return config
