"""Test cases for the __main__ module."""

import pytest
from click.testing import CliRunner
from click.testing import Result

from pytest_create.__main__ import main


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_with_defaults(runner: CliRunner) -> None:
    result: Result = runner.invoke(main, args=[])
    assert result.exit_code == 0


def test_main_with_cd_src(runner: CliRunner) -> None:
    result: Result = runner.invoke(main, args=["."])
    assert result.exit_code == 0


def test_main_with_cd_dst(runner: CliRunner) -> None:
    result: Result = runner.invoke(main, args=["."])
    assert result.exit_code == 0


def test_main_with_fake_src(runner: CliRunner) -> None:
    result: Result = runner.invoke(main, args=["foo", "."])
    assert result.exit_code == 0


def test_main_with_fake_dst(runner: CliRunner) -> None:
    result: Result = runner.invoke(main, args=[".", "foo"])
    assert result.exit_code == 0


def test_main_with_custom_src_and_dir(runner: CliRunner) -> None:
    result: Result = runner.invoke(main, args=["../src", "."])
    assert result.exit_code == 0


def test_main_with_fake_src_and_dst(runner: CliRunner) -> None:
    result: Result = runner.invoke(main, args=["foo", "foo"])
    assert result.exit_code == 0
