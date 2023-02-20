from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def unit_tests_dir() -> Path:
    return Path(__file__).parent


@pytest.fixture(scope="session")
def test_dir(tmp_path_factory):
    test_dir = tmp_path_factory.mktemp("test")
    (test_dir / "mod1.py").write_text("def func1(): return 'func1'")
    (test_dir / "pkg1").mkdir()
    (test_dir / "pkg1" / "__init__.py").touch()
    (test_dir / "pkg1" / "mod2.py").write_text("def func2(): return 'func2'")
    return test_dir
