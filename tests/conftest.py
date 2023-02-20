"""Pytest configuration file."""
import pathlib
from typing import Generator

import pytest


@pytest.fixture
def temp_module(tmp_path: pathlib.Path) -> Generator[pathlib.Path, None, None]:
    """Creates a temporary Python module."""
    module_file = tmp_path / "temp_module.py"
    module_file.write_text(
        "def temp_func(): return 1\n"
        "class TempClass: pass\n"
        "temp_variable = 'Hello'"
    )
    yield module_file
    module_file.unlink()
