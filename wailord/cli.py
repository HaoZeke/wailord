"""Console script for wailord."""
import sys
import click

from wailord.exp import cookies


@click.command()
@click.option("--conf", default=None, help="Configuration file in YAML")
@click.option(
    "--experiment",
    default="basicExperiment",
    help="Which experiment should be generated?",
)
def main(conf, experiment):
    """Console script for wailord."""
    cookies.gen_base(experiment, absolute=False, filen=conf)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
