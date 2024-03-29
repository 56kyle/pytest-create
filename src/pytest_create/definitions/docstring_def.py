"""A module used for rendering the source code of a Python Docstring."""
import re
from dataclasses import dataclass
from typing import Pattern


DOCSTRING_QUOTES_RE: Pattern[str] = re.compile(r'["\']+(.*?)["\']+')


@dataclass
class DocstringDef:
    """A class used for rendering the source code of a Python Docstring."""

    value: str = ""

    def __post_init__(self) -> None:
        """Remove the docstring quotes from the value."""
        self.value: str = self._remove_docstring_quotes(self.value)

    def __str__(self) -> str:
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
        return re.sub(DOCSTRING_QUOTES_RE, r"\1", value)

    def is_multi_line(self) -> bool:
        """Return True if the docstring contains a newline."""
        return "\n" in self.value

    def _format_as_single_line(self) -> str:
        return '"""' + self.value + '"""'

    def _format_as_multi_line(self) -> str:
        return '"""' + self.value + '\n"""'
