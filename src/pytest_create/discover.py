"""A Python library used for discovering objects in a path."""

import contextlib
import importlib.util
import inspect
import os
import pathlib
import pkgutil
from importlib.abc import MetaPathFinder
from importlib.abc import PathEntryFinder
from types import ModuleType
from typing import Any
from typing import AnyStr
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import Optional
from typing import Union

from loguru import logger


def find_objects(
    paths: Union[Iterable[AnyStr | pathlib.Path], AnyStr | pathlib.Path],
    prefix: str = "",
    filter_func: Optional[Callable[[Any], bool]] = None,
) -> Generator[Any, None, None]:
    """Find all objects in a path.

    This function looks for all packages and modules in a path,
    and then returns all objects within them.
    """
    paths_list: Optional[Iterable[str]]
    if (
        isinstance(paths, str)
        or isinstance(paths, bytes)
        or isinstance(paths, pathlib.Path)
    ):
        paths_list = [os.path.abspath(str(paths))]
    else:
        paths_list = [os.path.abspath(str(path)) for path in paths]
    logger.debug(f"Finding objects in {paths_list}")
    for importer, name, _ in pkgutil.walk_packages(path=paths_list, prefix=prefix):
        module = load_from_name(name, importer)
        if module:
            yield from find_module_objects(module, filter_func)


def load_from_name(
    name: str, finder: Union[PathEntryFinder, MetaPathFinder]
) -> Optional[ModuleType]:
    """Load a module from its name.

    Returns None if the module cannot be loaded.
    """
    logger.debug(f"Loading {name}")
    with contextlib.suppress(Exception):
        spec = finder.find_spec(name, None)
        if spec is None or spec.loader is None:
            logger.error(f"Failed to load module {name}")
            return None
        module: ModuleType = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None


def find_module_objects(
    module: ModuleType, filter_func: Optional[Callable[[Any], bool]] = None
) -> Generator[Any, None, None]:
    """Find all objects in a module."""
    logger.debug(f"Finding objects in module {module}")
    for _, obj in inspect.getmembers(module):
        if filter_func is None or filter_func(obj):
            yield obj
