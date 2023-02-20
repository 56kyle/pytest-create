import importlib.util
import pathlib
import pkgutil
from importlib.abc import PathEntryFinder

from src.pytest_create.discover import find_module_objects
from src.pytest_create.discover import find_objects
from src.pytest_create.discover import load_from_name


def test_find_objects(temp_module):
    """Tests the find_objects function."""
    path = pathlib.Path(temp_module).parent
    objects = list(find_objects(path))
    assert any(callable(obj) and obj.__name__ == "temp_func" for obj in objects)
    assert any(isinstance(obj, type) and obj.__name__ == "TempClass" for obj in objects)
    assert any(isinstance(obj, str) and obj == "Hello" for obj in objects)


def test_load_from_name(temp_module):
    """Tests the load_from_name function."""
    finder: PathEntryFinder = pkgutil.get_importer(str(temp_module.parent))
    assert load_from_name("temp_module", finder) is not None
    assert load_from_name("non_existent_module", finder) is None


def test_find_module_objects(temp_module):
    """Tests the find_module_objects function."""
    spec = importlib.util.spec_from_file_location("temp_module", temp_module)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    objects = list(find_module_objects(module))
    assert any(callable(obj) and obj.__name__ == "temp_func" for obj in objects)
    assert any(isinstance(obj, type) and obj.__name__ == "TempClass" for obj in objects)
    assert any(isinstance(obj, str) and obj == "Hello" for obj in objects)
