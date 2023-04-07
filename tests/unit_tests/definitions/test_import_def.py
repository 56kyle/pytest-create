from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import ModuleType

import pytest

from pytest_create.definitions.import_def import ImportDef
from tests.example_package.example_module import example_function


def create_module_from_file(path: Path) -> ModuleType:
    loader = SourceFileLoader("example_module", str(path))
    return loader.load_module()


@pytest.fixture(scope="module")
def example_module(example_package_dir: Path) -> ModuleType:
    return create_module_from_file(example_package_dir / "example_module.py")


def test_import_def_render_module_import(example_module: ModuleType) -> None:
    import_def: ImportDef = ImportDef(module=example_module)
    expected = "from tests.example_package import example_module"
    assert import_def.render() == expected


def test_import_def_render_object_import(example_module: ModuleType) -> None:
    import_def: ImportDef = ImportDef(module=example_module, obj=example_function)
    expected = "from tests.example_package.example_module import example_function"
    assert import_def.render() == expected


def test_import_def_render_object_import_with_str(example_module: ModuleType) -> None:
    import_def: ImportDef = ImportDef(module=example_module, obj="example_function")
    expected = "from tests.example_package.example_module import example_function"
    assert import_def.render() == expected


def test_import_def_render_object_import_with_object(
    example_module: ModuleType,
) -> None:
    import_def: ImportDef = ImportDef(module=example_module, obj=example_function)
    expected = "from tests.example_package.example_module import example_function"
    assert import_def.render() == expected


def test_import_def_render_object_import_without_name(
    example_module: ModuleType,
) -> None:
    obj = object()
    with pytest.raises(ValueError):
        import_def: ImportDef = ImportDef(module=example_module, obj=obj)
        import_def.render()


def test_import_def_find_package_root(
    example_module: ModuleType, example_package_dir: Path
) -> None:
    import_def: ImportDef = ImportDef(module=example_module)
    package_root = import_def._find_package_root()
    assert package_root.resolve() == example_package_dir / "example_module.py"
