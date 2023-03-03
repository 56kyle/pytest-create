from pathlib import Path
from typing import Optional

import pytest

from pytest_create.plugin import _get_default_dst
from pytest_create.plugin import _get_default_src
from pytest_create.plugin import _get_tests_dir
from pytest_create.plugin import is_in_tests_dir


class TestGetDefaultSrc:
    def test__get_default_src_with_no_tests(self, pytester: pytest.Pytester) -> None:
        default_src: Path = _get_default_src(config=pytester.parseconfig())
        assert default_src
        assert default_src == Path.cwd()

    def test__get_default_src_with_cwd_inside_tests(
        self, pytester: pytest.Pytester, config: pytest.Config
    ) -> None:
        original_path: Path = pytester.path
        pytester._path = pytester.path / "tests" / "unit_tests"
        pytester.chdir()
        default_src: Path = _get_default_src(config=config)
        assert default_src
        assert default_src == original_path.parent

    def test__get_default_src_with_cwd_outside_tests(
        self, config: pytest.Config
    ) -> None:
        default_src: Path = _get_default_src(config=config)
        assert default_src
        assert default_src == Path.cwd()


class TestGetDefaultDst:
    def test__get_default_dst_with_root_in_tests(self, config: pytest.Config) -> None:
        default_dst: Path = _get_default_dst(config=config)
        assert default_dst

    def test__get_default_dst_with_root_outside_tests(
        self, tests_dir: Path, config: pytest.Config, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(config, "_rootpath", tests_dir.parent)
        default_dst: Path = _get_default_dst(config=config)
        assert default_dst
        assert default_dst == tests_dir

    def test__get_default_dst_with_no_tests_dir(
        self, tmp_path: Path, config: pytest.Config, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(config, "_rootpath", tmp_path)
        default_dst: Path = _get_default_dst(config=config)
        assert default_dst
        assert default_dst == config.rootpath


class TestGetTestsDir:
    def test__get_tests_dir_with_rootpath_in_tests(self, config: pytest.Config) -> None:
        tests_dir: Optional[Path] = _get_tests_dir(config=config)
        assert tests_dir
        assert tests_dir.stem == "tests"

    def test__get_tests_dir_with_rootpath_outside_tests(
        self, config: pytest.Config
    ) -> None:
        config._rootpath = config._rootpath.parent.parent.parent
        tests_dir: Optional[Path] = _get_tests_dir(config=config)
        assert tests_dir
        assert tests_dir.stem == "tests"


class TestIsInTestsDir:
    def test_is_in_tests_dir_with_invalid(self) -> None:
        assert not is_in_tests_dir(Path("foo/bar"))

    def test_is_in_tests_dir_with_tests_at_end(self) -> None:
        assert not is_in_tests_dir(Path("foo/bar/tests"))

    def test_is_in_tests_dir_with_tests_only(self) -> None:
        assert not is_in_tests_dir(Path("tests"))

    def test_is_in_tests_dir_with_lower_case_tests(self) -> None:
        assert is_in_tests_dir(Path("foo/tests/bar"))

    def test_is_in_tests_dir_with_capitalized_tests(self) -> None:
        assert is_in_tests_dir(Path("foo/Tests/bar"))

    def test_is_in_tests_dir_with_tests_at_base(self) -> None:
        assert is_in_tests_dir(Path("tests/foo/bar"))
