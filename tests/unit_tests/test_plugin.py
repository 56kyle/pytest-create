from pathlib import Path

from pytest_create.plugin import is_in_tests_dir


class TestIsInTestsDir:
    def test_is_in_tests_dir_with_invalid(self):
        assert not is_in_tests_dir(Path("foo/bar"))

    def test_is_in_tests_dir_with_lower_case_tests(self):
        assert is_in_tests_dir(Path("foo/tests/bar"))

    def test_is_in_tests_dir_with_capitalized_tests(self):
        assert is_in_tests_dir(Path("foo/Tests/bar"))

    def test_is_in_tests_dir_with_tests_at_base(self):
        assert is_in_tests_dir(Path("tests/foo/bar"))

    def test_is_in_tests_dir_with_tests_at_end(self):
        assert is_in_tests_dir(Path("foo/bar/tests"))

    def test_is_in_tests_dir_with_tests_only(self):
        assert is_in_tests_dir(Path("tests"))
