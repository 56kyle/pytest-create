"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """pytest-create."""


if __name__ == "__main__":
    main(prog_name="pytest-create")  # pragma: no cover
