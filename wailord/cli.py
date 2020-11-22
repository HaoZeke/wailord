"""Console script for wailord."""
import sys
import click

from wailord.exp import cookies


@click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--conf', prompt='Input file',
#               help='Configuration file in TOML, YAML, DOTENV or JSON')
@click.option(
    "--conf", default=None, help="Configuration file in TOML, YAML, DOTENV or JSON"
)
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

# @click.command()
# @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)

# if __name__ == '__main__':
#     hello()
