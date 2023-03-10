"""Command-line interface."""
from typing import List

import click
import pytest
from loguru import logger


@click.command(name="pytest-create")
@click.argument(
    "src", type=click.Path(file_okay=True, dir_okay=True), default="", required=False
)
@click.argument(
    "dst",
    type=click.Path(file_okay=True, dir_okay=True),
    default="",
    required=False,
)
def main(src: click.Path, dst: click.Path) -> None:
    """Create new unit tests for the specified source file or directory."""
    logger.debug("Running main from CLI")
    logger.debug(f"src - {src}\ndst - {dst}")
    dst_args: List[str] = [str(dst)] if dst else []
    pytest.main(
        args=[*dst_args, "--create" if not src else f"--create={str(src)}"],
        plugins=["pytest_create.plugin"],
    )


if __name__ == "__main__":
    main(prog_name="pytest-create")  # pragma: no cover
