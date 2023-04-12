"""A module used for rendering the source code of a Python Import."""
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from types import ModuleType


@dataclass
class ImportDef:
    """A class used for rendering the source code of a Python Import."""

    module: ModuleType
    obj: object = None
    module_path: Path = field(init=False)
    relative_module_path: Path = field(init=False)
    module_parent: str = field(init=False)

    def __post_init__(self) -> None:
        """Set the module path, relative module path and module parent."""
        self.module_path: Path = Path(getattr(self.module, "__file__", ""))
        self.relative_module_path: Path = self._find_package_root()
        self.module_parent: str = ".".join(
            self.relative_module_path.with_suffix("").parts[:-1]
        )

    def render(self) -> str:
        """Render the import statement for the object."""
        if self.obj is None:
            return self._render_module_import()
        return self._render_object_import()

    def _render_module_import(self) -> str:
        return f"from {self.module_parent} import {self.relative_module_path.stem}"

    def _render_object_import(self) -> str:
        object_module: str = ".".join(self.relative_module_path.with_suffix("").parts)
        if isinstance(self.obj, str):
            return f"from {object_module} import {self.obj}"
        if not hasattr(self.obj, "__name__"):
            raise ValueError(f"Object must have a name to import - {self.obj}")
        return f"from {object_module} import {getattr(self.obj, '__name__', '')}"

    def _find_package_root(self) -> Path:
        current_root: Path = self.module_path
        while (current_root.parent / "__init__.py").exists():
            current_root = current_root.parent
        current_root = current_root.parent
        return self.module_path.relative_to(current_root)
