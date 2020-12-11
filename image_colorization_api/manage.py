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
#     """Create a new admin user"""
#     from image_colorization_api.extensions import db
#     from image_colorization_api.models import User

#     click.echo("create user")
#     user = User(username="d", email="dannykpark@gmail.com", password="swingbatta1", active=True)
#     db.session.add(user)
#     db.session.commit()
#     click.echo("created user admin")


if __name__ == "__main__":
    cli()
