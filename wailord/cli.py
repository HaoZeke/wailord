"""Console script for wailord."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for wailord."""
    click.echo("Replace this message by putting your code into "
               "wailord.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
