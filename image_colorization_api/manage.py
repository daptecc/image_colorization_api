import click
from flask.cli import FlaskGroup

from image_colorization_api.app import create_app


def create_image_colorization_api(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_image_colorization_api)
def cli():
    """Main entry point"""

@cli.command("init")
def init():
    pass

if __name__ == "__main__":
    cli()
