"""A module used for rendering the source code of a Python Docstring."""
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class DocstringDef:
    """A class used for rendering the source code of a Python Docstring."""

    value: Optional[str] = None
    docstring_quotes_re: re.Pattern = re.compile(r'["\']+(.*?)["\']+')

    def __post_init__(self):
        """Remove the docstring quotes from the value."""
        if self.value is None:
            self.value: str = ""
        self.value: str = self._remove_docstring_quotes(self.value)

    def __str__(self):
        """Return the rendered docstring."""
        return self.render()

    def render(self) -> str:
        """Return the rendered docstring."""
        if not self.value:
            return ""
        if self.is_multi_line():
            return self._format_as_multi_line()
        return self._format_as_single_line()

    @classmethod
    def from_string(cls, value: str) -> "DocstringDef":
        """Create a DocstringDef from a string."""
        return cls(value=value)

    @classmethod
    def _remove_docstring_quotes(cls, value: str) -> str:
        """Remove the docstring quotes from a string."""
        return re.sub(cls.docstring_quotes_re, r"\1", value)

    def is_multi_line(self) -> bool:
        """Return True if the docstring contains a newline."""
        return "\n" in self.value

    def _format_as_single_line(self) -> str:
        return f'"""{self.value!r}"""'

    def _format_as_multi_line(self) -> str:
        return f'"""{self.value}\n"""'
