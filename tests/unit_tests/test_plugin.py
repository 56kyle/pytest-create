from pathlib import Path

import pytest

from pytest_create.plugin import _get_default_dst
from pytest_create.plugin import _get_default_src
from pytest_create.plugin import _get_tests_dir
from pytest_create.plugin import is_in_tests_dir


class TestGetDefaultSrc:
    def test__get_default_src_with_no_tests(self, pytester: pytest.Pytester):
        default_src: Path = _get_default_src(config=pytester.parseconfig())
        assert default_src
        assert default_src == Path.cwd()

    def test__get_default_src_with_cwd_inside_tests(
        self, pytester: pytest.Pytester, config: pytest.Config
    ):
        original_path: Path = pytester.path
        pytester._path = pytester.path / "tests" / "unit_tests"
        pytester.chdir()
        default_src: Path = _get_default_src(config=config)
        assert default_src
        assert default_src == original_path.parent

    def test__get_default_src_with_cwd_outside_tests(self, config: pytest.Config):
        default_src: Path = _get_default_src(config=config)
        assert default_src
        assert default_src == Path.cwd()


class TestGetDefaultDst:
    def test__get_default_dst_with_default_src(self, config: pytest.Config):
        default_dst: Path = _get_default_dst(config=config)
        assert default_dst


class TestGetTestsDir:
    def test__get_tests_dir_with_rootpath_in_tests(self, config: pytest.Config):
        tests_dir: Path = _get_tests_dir(config=config)
        assert tests_dir
        assert tests_dir.stem == "tests"

    def test__get_tests_dir_with_rootpath_outside_tests(self, config: pytest.Config):
        config._rootpath = config._rootpath.parent.parent.parent
        tests_dir: Path = _get_tests_dir(config=config)
        assert tests_dir
        assert tests_dir.stem == "tests"


class TestIsInTestsDir:
    def test_is_in_tests_dir_with_invalid(self):
        assert not is_in_tests_dir(Path("foo/bar"))

    def test_is_in_tests_dir_with_tests_at_end(self):
        assert not is_in_tests_dir(Path("foo/bar/tests"))

    def test_is_in_tests_dir_with_tests_only(self):
        assert not is_in_tests_dir(Path("tests"))

    def test_is_in_tests_dir_with_lower_case_tests(self):
        assert is_in_tests_dir(Path("foo/tests/bar"))

    def test_is_in_tests_dir_with_capitalized_tests(self):
        assert is_in_tests_dir(Path("foo/Tests/bar"))

    def test_is_in_tests_dir_with_tests_at_base(self):
        assert is_in_tests_dir(Path("tests/foo/bar"))
