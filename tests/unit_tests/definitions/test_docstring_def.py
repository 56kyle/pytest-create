import pytest

from pytest_create.definitions.docstring_def import DocstringDef


def test_empty_docstring() -> None:
    docstring = DocstringDef()
    assert str(docstring) == ""
    assert docstring.render() == ""


def test_single_line_docstring() -> None:
    docstring = DocstringDef(value="This is a single-line docstring.")
    assert str(docstring) == '"""This is a single-line docstring."""'
    assert docstring.render() == '"""This is a single-line docstring."""'


def test_multi_line_docstring() -> None:
    docstring = DocstringDef(value="This is a\nmulti-line docstring.")
    assert str(docstring) == '"""This is a\nmulti-line docstring.\n"""'
    assert docstring.render() == '"""This is a\nmulti-line docstring.\n"""'


def test_from_string() -> None:
    docstring = DocstringDef.from_string("This is a single-line docstring.")
    assert isinstance(docstring, DocstringDef)
    assert docstring.value == "This is a single-line docstring."


def test_remove_docstring_quotes() -> None:
    value = '"""This is a docstring with quotes."""'
    result = DocstringDef._remove_docstring_quotes(value)
    assert result == "This is a docstring with quotes."


@pytest.mark.parametrize(
    "value, expected",
    [
        ("This is a single-line docstring.", False),
        ("This is a\nmulti-line docstring.", True),
    ],
)
def test_is_multi_line(value: str, expected: bool) -> None:
    docstring = DocstringDef(value=value)
    assert docstring.is_multi_line() == expected
