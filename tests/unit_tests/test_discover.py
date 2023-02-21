import importlib.util
import pkgutil
from importlib.abc import PathEntryFinder
from pathlib import Path
from typing import Any
from typing import Optional

from pytest_create.discover import find_module_objects
from pytest_create.discover import find_objects
from pytest_create.discover import load_from_name
from src.example_package.example_module import ExampleClass
from src.example_package.example_module import example_function
from src.example_package.example_module import example_variable


def get_names(objects: list[Any]) -> list[str]:
    return [getattr(obj, "__name__", None) for obj in objects]


class TestFindObjects:
    def test_find_objects(self, example_package_dir) -> None:
        objects: list[Any] = list(find_objects(example_package_dir))
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_prefix(self, example_package_dir) -> None:
        """Tests the find_objects function with a prefix."""
        objects: list[Any] = list(
            find_objects(example_package_dir, prefix="example_package.")
        )
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_filter(self, example_package_dir) -> None:
        """Tests the find_objects function with a filter."""
        objects: list[Any] = list(
            find_objects(
                example_package_dir, filter_func=lambda obj: isinstance(obj, str)
            )
        )
        assert example_variable in objects
        assert example_function.__name__ not in get_names(objects)
        assert ExampleClass not in objects

    def test_find_objects_with_iterable(self, example_package_dir) -> None:
        """Tests the find_objects function with an iterable."""
        objects: list[Any] = list(find_objects([example_package_dir]))
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_str(self, example_package_dir) -> None:
        """Tests the find_objects function with a string."""
        objects: list[Any] = list(find_objects(str(example_package_dir)))
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_path(self, example_package_dir) -> None:
        """Tests the find_objects function with a Path."""
        objects: list[Any] = list(find_objects(example_package_dir))
        assert example_function.__name__ in get_names(objects)

    def test_find_objects_with_module_not_found(
        self, example_package_dir, monkeypatch
    ) -> None:
        monkeypatch.setattr("pytest_create.discover.load_from_name", lambda *args: None)
        objects: list[Any] = list(find_objects(example_package_dir))
        assert not objects

    def test_find_objects_invalid_path(self) -> None:
        """Tests the find_objects function with an invalid path."""
        path = Path("non_existent_path")
        assert not list(find_objects(path))


class TestLoadFromName:
    def test_load_from_name(self, example_package_dir) -> None:
        """Tests the load_from_name function."""
        module = load_from_name(
            "example_module", pkgutil.get_importer(str(example_package_dir))
        )
        assert callable(module.example_function)
        assert isinstance(module.ExampleClass, type)
        assert module.example_variable == ""

    def test_load_from_name_with_spec_not_found(
        self, example_package_dir, monkeypatch
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
        self, example_package_dir, monkeypatch
    ) -> None:
        """Tests the load_from_name function with an error on spec load."""
        finder: Optional[PathEntryFinder] = pkgutil.get_importer(
            str(example_package_dir)
        )
        assert finder is not None
        monkeypatch.setattr(finder, "find_spec", lambda *args: int(1) / 2)
        module = load_from_name("non_existent_module", finder)
        assert module is None


def test_find_module_objects(example_module_spec) -> None:
    """Tests the find_module_objects function."""
    module = importlib.util.module_from_spec(example_module_spec)
    example_module_spec.loader.exec_module(module)
    objects = list(find_module_objects(module))
    assert example_function.__name__ in get_names(objects)
    assert example_variable in objects
    assert ExampleClass.__name__ in get_names(objects)
