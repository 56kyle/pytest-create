import importlib.util
import inspect
import pkgutil
from importlib.abc import MetaPathFinder
from importlib.abc import PathEntryFinder
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Union

import pytest
from _pytest.monkeypatch import MonkeyPatch

import pytest_create.util
from pytest_create.util import SourceFileCompatible
from pytest_create.util import find_module_objects
from pytest_create.util import find_modules
from pytest_create.util import find_objects
from pytest_create.util import find_sub_modules
from pytest_create.util import get_source_code_filter
from pytest_create.util import is_object_defined_under_path
from pytest_create.util import load_from_name
from pytest_create.util import standardize_paths
from tests.example_package.example_module import ExampleClass
from tests.example_package.example_module import example_function
from tests.example_package.example_module import example_variable
from tests.example_package.example_sub_package.example_sub_module import (
    example_function_b,
)
from tests.example_package.example_sub_package.example_sub_module import (
    example_variable_b,
)


def get_names(objects: List[Any]) -> List[Any]:
    return [getattr(obj, "__name__", None) for obj in objects]


class TestGetSourceCodeFilter:
    def test_get_source_code_filter_with_objects(
        self, example_package_dir: Path
    ) -> None:
        src_filter: Callable[[SourceFileCompatible], bool] = get_source_code_filter(
            src=example_package_dir
        )

        objects: List[Any] = list(
            find_objects(example_package_dir, filter_func=src_filter)
        )
        assert example_variable not in objects
        assert example_function.__name__ in get_names(objects)
        assert example_variable_b not in objects
        assert example_function_b.__name__ in get_names(objects)
        assert len(objects) == 4

    def test_get_source_code_filter_with_no_source_file(
        self, example_package_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        src_filter: Callable[[SourceFileCompatible], bool] = get_source_code_filter(
            src=example_package_dir
        )
        assert src_filter(example_function) is True
        monkeypatch.setattr(inspect, "getsourcefile", lambda obj: None)
        assert src_filter(example_function) is False


class TestIsObjectDefinedUnderPath:
    def test_is_object_defined_under_path_with_object_under_path(
        self, example_package_dir: Path
    ) -> None:
        assert (
            is_object_defined_under_path(obj=example_function, src=example_package_dir)
            is True
        )

    def test_is_object_defined_under_path_with_object_under_relative_path(
        self,
        example_package_dir: Path,
        monkeypatch: pytest.MonkeyPatch,
        tests_dir: Path,
    ) -> None:
        src_string: Optional[str] = inspect.getsourcefile(example_function)
        assert src_string is not None
        original_source_file: Path = Path(src_string)
        monkeypatch.setattr(
            inspect,
            "getsourcefile",
            lambda obj: original_source_file.relative_to(tests_dir),
        )
        assert (
            is_object_defined_under_path(obj=example_function, src=example_package_dir)
            is False
        )


class TestStandardizePaths:
    def test_standardize_paths_with_str(self, example_package_dir: Path) -> None:
        assert standardize_paths(str(example_package_dir)) == [str(example_package_dir)]

    def test_standardize_paths_with_path(self, example_package_dir: Path) -> None:
        assert standardize_paths(example_package_dir) == [str(example_package_dir)]

    def test_standardize_paths_with_iterable_str(
        self, example_package_dir: Path
    ) -> None:
        assert standardize_paths([str(example_package_dir)]) == [
            str(example_package_dir)
        ]

    def test_standardize_paths_with_iterable_path(
        self, example_package_dir: Path
    ) -> None:
        assert standardize_paths([example_package_dir]) == [str(example_package_dir)]


class TestFindObjects:
    def test_find_objects(self, example_package_dir: Path) -> None:
        objects: List[Any] = list(find_objects(example_package_dir))
        assert example_function.__name__ in get_names(objects)

    def test_find_source_objects(self, example_package_dir: Path) -> None:
        objects: List[Any] = list(
            find_objects(
                example_package_dir,
                filter_func=get_source_code_filter(example_package_dir),
            )
        )
        assert len(objects) == len(set(objects))

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
        monkeypatch.setattr("pytest_create.util.load_from_name", lambda *args: None)
        objects: List[Any] = list(find_objects(example_package_dir))
        assert not objects

    def test_find_objects_invalid_path(self) -> None:
        """Tests the find_objects function with an invalid path."""
        path = Path("non_existent_path")
        assert not list(find_objects(path))


class TestFindModules:
    def test_find_modules(self, example_package_dir: Path) -> None:
        modules: List[ModuleType] = list(find_modules(example_package_dir))
        assert len(modules) == len(set(modules))
        assert set(get_names(modules)) == {
            "example_module",
            "example_sub_package",
            "example_sub_module",
        }

    def test_find_modules_with_none(self, tmp_path: Path) -> None:
        modules: List[ModuleType] = list(find_modules(tmp_path))
        assert modules == []


class TestFindSubModules:
    def test_find_sub_modules(self, example_package_dir: Path) -> None:
        pass

    def test_find_sub_modules_with_none(self, example_package_data_dir: Path) -> None:
        assert {*find_sub_modules(example_package_data_dir)} == set()

    def test_find_sub_modules_with_nested_package(
        self, example_package_dir: Path
    ) -> None:
        modules: List[ModuleType] = [*find_sub_modules(example_package_dir)]
        assert {*get_names(modules)} == {"example_module", "example_sub_package"}

    def test_find_sub_modules_with_unable_to_load(
        self, example_package_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def fake_load_from_name(
            name: str, finder: Union[PathEntryFinder, MetaPathFinder]
        ) -> Optional[ModuleType]:
            if name == "example_module":
                return None
            return load_from_name(name=name, finder=finder)

        monkeypatch.setattr(pytest_create.util, "load_from_name", fake_load_from_name)

        modules: List[ModuleType] = [*find_sub_modules(example_package_dir)]
        assert {*get_names(modules)} == {"example_sub_package"}


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
