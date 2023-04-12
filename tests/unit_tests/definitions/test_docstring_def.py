import pytest

from pytest_create.definitions.docstring_def import DocstringDef


@pytest.mark.parametrize(
    argnames=["docstring_def", "expected"],
    argvalues=[
        ["", ""],
        ["This is a single-line docstring.", '"""This is a single-line docstring."""'],
        [
            "This is a\nmulti-line docstring.",
            '"""This is a\nmulti-line docstring.\n"""',
        ],
    ],
    ids=["empty_docstring", "single_line_docstring", "multi_line_docstring"],
    indirect=["docstring_def"],
)
def test_render(docstring_def: DocstringDef, expected: str) -> None:
    assert docstring_def.render() == expected


@pytest.mark.parametrize(
    argnames=["docstring_def", "expected"],
    argvalues=[
        ["", ""],
        ["This is a single-line docstring.", '"""This is a single-line docstring."""'],
        [
            "This is a\nmulti-line docstring.",
            '"""This is a\nmulti-line docstring.\n"""',
        ],
    ],
    ids=["empty_docstring", "single_line_docstring", "multi_line_docstring"],
    indirect=["docstring_def"],
)
def test_str(docstring_def: DocstringDef, expected: str) -> None:
    assert str(docstring_def) == expected


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
