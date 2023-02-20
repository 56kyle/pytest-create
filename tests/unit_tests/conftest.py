from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def unit_tests_dir() -> Path:
    return Path(__file__).parent
