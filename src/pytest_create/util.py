"""A Python library used for discovering objects in a path."""

import contextlib
import importlib.util
import inspect
import os
import pathlib
import pkgutil
from importlib.abc import MetaPathFinder
from importlib.abc import PathEntryFinder
from types import CodeType
from types import FrameType
from types import FunctionType
from types import MethodType
from types import ModuleType
from types import TracebackType
from typing import Any
from typing import AnyStr
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from loguru import logger


SourceFileCompatible = TypeVar(
    "SourceFileCompatible",
    ModuleType,
    Type[Any],
    MethodType,
    FunctionType,
    TracebackType,
    FrameType,
    CodeType,
    Callable[..., Any],
)


def get_source_code_filter(src: pathlib.Path) -> Callable[[SourceFileCompatible], bool]:
    """Returns a filter for objects defined in a file under the 'src' path."""
    return lambda obj: is_object_defined_under_path(obj=obj, src=src)


def is_object_defined_under_path(obj: SourceFileCompatible, src: pathlib.Path) -> bool:
    """Filters for objects defined in a file under the 'src' path."""
    try:
        obj_file: Optional[str] = inspect.getsourcefile(obj)
    except TypeError:
        if isinstance(obj, type):
            return obj.__module__ != "builtins"
        return False

    if obj_file is None:
        return False

    obj_path = pathlib.Path(obj_file)
    if not obj_path.is_absolute():
        return False

    src_path: pathlib.Path = src if src.is_absolute() else src.resolve()

    if not obj_path.parent.samefile(src_path) and not obj_path.parent.is_relative_to(
        src_path
    ):
        return False

    return (
        bool(obj_path.relative_to(src_path))
        if obj_path.is_absolute()
        else obj_path in src_path.iterdir()
    )


def find_objects(
    paths: Union[Iterable[Union[AnyStr, pathlib.Path]], AnyStr, pathlib.Path],
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
