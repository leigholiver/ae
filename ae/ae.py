import click
from click_aliases import ClickAliasedGroup

from . import config
from . import __version__
from .aws import session

description="""\b
ae v%s
AWS Extended
""" % str(__version__)

@click.group(cls=ClickAliasedGroup, help=description)
@click.option('--aws-profile', '-p', envvar='AWS_PROFILE', help='AWS CLI profile to use')
def ae(aws_profile):
    config.load(aws_profile)
    # init root mfa if req
    session.client("sts")
