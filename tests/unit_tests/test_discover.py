import importlib.util
import pkgutil
from importlib.abc import PathEntryFinder
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Any
from typing import List
from typing import Optional

from _pytest.monkeypatch import MonkeyPatch

from pytest_create.discover import find_module_objects
from pytest_create.discover import find_objects
from pytest_create.discover import load_from_name
from tests.example_package.example_module import ExampleClass
from tests.example_package.example_module import example_function
from tests.example_package.example_module import example_variable


def get_names(objects: List[Any]) -> List[Any]:
    return [getattr(obj, "__name__", None) for obj in objects]


class TestFindObjects:
    def test_find_objects(self, example_package_dir: Path) -> None:
        objects: List[Any] = list(find_objects(example_package_dir))
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_prefix(self, example_package_dir: Path) -> None:
        """Tests the find_objects function with a prefix."""
        objects: List[Any] = list(
            find_objects(example_package_dir, prefix="example_package.")
        )
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_filter(self, example_package_dir: Path) -> None:
        """Tests the find_objects function with a filter."""
        objects: List[Any] = list(
            find_objects(
                example_package_dir, filter_func=lambda obj: isinstance(obj, str)
            )
        )
        assert example_variable in objects
        assert example_function.__name__ not in get_names(objects)
        assert ExampleClass not in objects

    def test_find_objects_with_iterable(self, example_package_dir: Path) -> None:
        """Tests the find_objects function with an iterable."""
        objects: List[Any] = list(find_objects([example_package_dir]))
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_str(self, example_package_dir: Path) -> None:
        """Tests the find_objects function with a string."""
        objects: List[Any] = list(find_objects(str(example_package_dir)))
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_path(self, example_package_dir: Path) -> None:
        """Tests the find_objects function with a Path."""
        objects: List[Any] = list(find_objects(example_package_dir))
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_module_not_found(
        self, example_package_dir: Path, monkeypatch: MonkeyPatch
    ) -> None:
        monkeypatch.setattr("pytest_create.discover.load_from_name", lambda *args: None)
        objects: List[Any] = list(find_objects(example_package_dir))
        assert not objects

    def test_find_objects_invalid_path(self) -> None:
        """Tests the find_objects function with an invalid path."""
        path = Path("non_existent_path")
        assert not list(find_objects(path))


class TestLoadFromName:
    def test_load_from_name(self, example_package_dir: Path) -> None:
        """Tests the load_from_name function."""
        finder: Optional[PathEntryFinder] = pkgutil.get_importer(
            str(example_package_dir)
        )
        assert finder is not None
        module = load_from_name("example_module", finder)
        assert module is not None
        assert callable(module.example_function)
        assert isinstance(module.ExampleClass, type)
        assert isinstance(module.example_variable, str)

    def test_load_from_name_with_spec_not_found(
        self, example_package_dir: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests the load_from_name function with a spec not found."""
        finder: Optional[PathEntryFinder] = pkgutil.get_importer(
            str(example_package_dir)
        )
        assert finder is not None
        monkeypatch.setattr(finder, "find_spec", lambda *args: None)
        module = load_from_name("non_existent_module", finder)
        assert module is None

    def test_load_from_name_with_error_on_spec_load(
        self, example_package_dir: Path, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests the load_from_name function with an error on spec load."""
        finder: Optional[PathEntryFinder] = pkgutil.get_importer(
            str(example_package_dir)
        )
        assert finder is not None
        monkeypatch.setattr(finder, "find_spec", lambda *args: int(1) / 2)
        module: Optional[ModuleType] = load_from_name("non_existent_module", finder)
        assert module is None


def test_find_module_objects(example_module_spec: ModuleSpec) -> None:
    """Tests the find_module_objects function."""
    module: ModuleType = importlib.util.module_from_spec(example_module_spec)
    assert example_module_spec.loader is not None
    example_module_spec.loader.exec_module(module)
    objects: List[Any] = list(find_module_objects(module))
    assert example_function.__name__ in get_names(objects)
    assert example_variable in objects
    assert ExampleClass.__name__ in get_names(objects)