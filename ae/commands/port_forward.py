import click
import re
import sys

from .. import ae
from ..aws import ec2
from ..decorators import find_resources

description = """\b
Forward a local port to a remote port on an instance/container
"""

@ae.command(
    name="port-forward",
    aliases=["pf"],
    help=description
)
@click.argument("resource")
@click.argument("ports")
@find_resources("resource", kinds=["ec2", "ecs"])
def port_forward(resource, ports):

    result = re.search(r"([0-9]+)(?::([0-9]+))?", ports)
    if not result:
        print(f"Invalid port combination {ports}")
        sys.exit(1)

    local, remote = result.groups()
    remote = remote if remote else local
    ec2.port_forward(resource, local, remote)
