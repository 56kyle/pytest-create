"""Python module for creating pytests from python objects."""
from pathlib import Path

from loguru import logger


def create_tests(src: Path, dst: Path) -> None:
    """Create test files for the specified package module.

    The created test files will be located in the specified destination
    directory.
    """
    logger.debug("create_tests -")
    logger.debug(f"\tsrc - {src}")
    logger.debug(f"\tdst - {dst}")
