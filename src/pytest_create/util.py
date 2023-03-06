"""A Python library used for discovering objects in a path."""

import contextlib
import importlib.util
import inspect
import os
import pathlib
import pkgutil
from importlib.abc import MetaPathFinder
from importlib.abc import PathEntryFinder
from importlib.machinery import ModuleSpec
from types import CodeType
from types import FrameType
from types import FunctionType
from types import MethodType
from types import ModuleType
from types import TracebackType
from typing import Any
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import List
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


SupportsPath = TypeVar("SupportsPath", str, pathlib.Path)


def get_source_code_filter(src: pathlib.Path) -> Callable[[SourceFileCompatible], bool]:
    """Returns a filter for objects defined in a file under the 'src' path."""
    return lambda obj: is_object_defined_under_path(obj=obj, src=src) and is_src_object(
        obj
    )


def is_src_object(obj: SourceFileCompatible) -> bool:
    """Returns if obj is a source code definition or not."""
    if inspect.ismodule(obj):
        # If the object is a module, check if its __file__ attribute is not None
        return getattr(obj, "__file__", None) is not None

    elif inspect.isfunction(obj) or inspect.isclass(obj) or isinstance(obj, type):
        # If the object is a function, class, or type,
        # get the module where it was defined
        module: Optional[ModuleType] = inspect.getmodule(obj)
        if module is None:
            # If the module is None,
            # it means that the object was defined in the __main__ module
            return True
        else:
            # Check if the module's __file__ attribute is not None
            return getattr(module, "__file__", None) is not None

    elif isinstance(obj, CodeType):
        # If the object is a code object, check its co_filename attribute
        return obj.co_filename is not None

    elif isinstance(obj, FrameType):
        # If the object is a frame,
        # check if its f_code attribute corresponds to a source code object
        return is_src_object(obj.f_code)

    else:
        # For all other types of objects, assume they are not source objects
        return False


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

    if is_relative_to(obj_path, src_path):
        return True
    return obj_path.parent.samefile(src_path)


def is_relative_to(path: pathlib.Path, other: pathlib.Path) -> bool:
    """The same as pathlib.Path.is_relative_to but usable in python 3.6."""
    try:
        path.relative_to(other)
    except ValueError:
        return False
    return True


def standardize_paths(paths: Union[Iterable[SupportsPath], SupportsPath]) -> List[str]:
    """Standardizes the input for paths for use in pkgutil methods."""
    paths_list: Optional[Iterable[str]]
    if isinstance(paths, str):
        return [os.path.abspath(str(paths))]
    if isinstance(paths, pathlib.Path):
        return [os.path.abspath(str(paths))]
    return [os.path.abspath(str(path)) for path in paths]


def find_objects(
    paths: Union[Iterable[SupportsPath], SupportsPath],
    prefix: str = "",
    filter_func: Optional[Callable[[Any], bool]] = None,
) -> Generator[Any, None, None]:
    """Find all objects in a path.

    This function looks for all packages and modules in a path,
    and then returns all objects within them.
    """
    for module in find_modules(paths=standardize_paths(paths), prefix=prefix):
        yield from find_module_objects(module=module, filter_func=filter_func)


def find_modules(
    paths: Union[Iterable[SupportsPath], SupportsPath],
    prefix: str = "",
) -> Generator[ModuleType, None, None]:
    """Find all objects in a path.

    This function looks for all packages and modules in a path,
    and then returns all objects within them.
    """
    logger.debug(f"Finding objects in {paths}")
    for importer, name, ispkg in pkgutil.walk_packages(
        path=standardize_paths(paths), prefix=prefix
    ):
        module = load_from_name(name, importer)
        if module:
            if ispkg:
                yield from find_sub_modules(module.__path__)
            yield module


def find_sub_modules(
    paths: Union[Iterable[SupportsPath], SupportsPath]
) -> Generator[ModuleType, None, None]:
    """Iterates over all submodules of the provided module if it is a package."""
    for sub_module_info in pkgutil.iter_modules(path=standardize_paths(paths)):
        sub_module: Optional[ModuleType] = load_from_name(
            sub_module_info.name, sub_module_info.module_finder
        )
        if sub_module is not None:
            yield sub_module


def load_from_name(
    name: str, finder: Union[PathEntryFinder, MetaPathFinder]
) -> Optional[ModuleType]:
    """Load a module from its name.

    Returns None if the module cannot be loaded.
    """
    logger.debug(f"Loading {name}")
    with contextlib.suppress(Exception):
        spec: ModuleSpec = finder.find_spec(name, None)
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
    logger.debug(f"Searching {module.__name__}...")
    for _, obj in inspect.getmembers(module):
        if filter_func is None or filter_func(obj):
            yield obj
