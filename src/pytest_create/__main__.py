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
    type=click.Path(file_okay=True, dir_okay=True, exists=True),
    default="",
    required=False,
)
def main(src: click.Path, dst: click.Path) -> None:
    """Create new unit tests for the specified source file or directory."""
    logger.debug("Running main from CLI")
    logger.debug(f"src - {src}\ndst - {dst}")
    args: List[str] = ["--create"]
    if src:
        args.append(str(src))
    if dst:
        args.append(str(dst))
    pytest.main(args=args, plugins=["pytest_create.plugin"])


if __name__ == "__main__":
    main(prog_name="pytest-create")  # pragma: no cover
