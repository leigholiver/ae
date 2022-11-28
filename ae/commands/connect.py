import click

from .. import ae
from ..decorators import find_resources
from ..aws import ec2
from ..aws import ecs

description = """\b
Connect to a resource via CLI
"""

@ae.command(
    name="connect",
    aliases=["c", "sh"],
    help=description
)
@click.argument("resource")
@find_resources("resource", kinds=["ec2", "ecs"])
def connect(resource):
    match resource["Kind"]:
        case "ec2":
            ec2.connect(resource)
        case "ecs":
            ecs.connect(resource)
