"""A Python library used for discovering objects in a path."""
# Path: src\pytest_create\discover.py

import contextlib
import importlib.util
import inspect
import pathlib
import pkgutil
from importlib.abc import PathEntryFinder
from types import ModuleType
from typing import Any
from typing import Callable
from typing import Generator
from typing import Optional

from loguru import logger


def find_objects(
    path: pathlib.Path, filter_func: Callable[[Any], bool] = None
) -> Generator[Any, None, None]:
    """Find all objects in a path.

    This function looks for all packages and modules in a path,
    and then returns all objects within them.
    """
    logger.debug(f"Finding objects in {path}")
    for importer, name, _ in pkgutil.walk_packages(path=[str(path)]):
        module = load_from_name(name, importer)
        if module:
            yield from find_module_objects(module, filter_func)


def load_from_name(name: str, finder: PathEntryFinder) -> Optional[ModuleType]:
    """Load a module from its name.

    Returns None if the module cannot be loaded.
    """
    logger.debug(f"Loading {name}")
    with contextlib.suppress(Exception):
        spec = finder.find_spec(name)
        if spec is None:
            logger.error(f"Failed to load module {name}")
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def find_module_objects(
    module: ModuleType, filter_func: Callable[[Any], bool] = None
) -> Generator[Any, None, None]:
    """Find all objects in a module."""
    logger.debug(f"Finding objects in module {module}")
    for _, obj in inspect.getmembers(module):
        if filter_func is None or filter_func(obj):
            yield obj


if __name__ == "__main__":
    for obj in find_objects(pathlib.Path.cwd().parent):
        try:
            logger.info(f"{obj.__module__} - {obj.__name__}")
        except AttributeError:
            pass
