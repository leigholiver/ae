import click
import sys

from .. import ae
from ..aws import ec2
from ..aws import ecs
from ..decorators import find_resources
from InquirerPy import inquirer
from InquirerPy.base import Choice

description = """\b
Run a command on instances/tasks
"""

def _build_command(ctx, param, value):
    return " ".join(value).strip()

def _get_result_output(result):
    output = f"\n - {result['Ident']} ({result['Status']})\n{result['StdOut']}\n"
    if result["StdErr"] != "":
        output += f"{result['StdErr']}\n"
    return output

@ae.command(
    name="run-command",
    aliases=["rc", "exec"],
    help=description
)
@click.argument("resources")
@click.argument("command", nargs=-1, callback=_build_command)
@find_resources("resources", kinds=["ec2", "ecs"], single=False)
def run_command(resources, command):

    # make sure we have a command to run
    if command == "":
        print("You must specify a command to run")
        sys.exit(1)

    if len(resources) > 1:
        choices = inquirer.checkbox(
            message=f"""Do you want to run `{command}` against these resources?
Space to toggle, Enter to continue, Ctrl + C to abort...
""",
            choices=[
                Choice(r["Ident"], enabled=True)
                for r in resources
            ],
            validate=lambda result: len(result) >= 1,
            transformer=lambda result: f"{len(result)} resource{'s' if len(result) > 1 else ''} selected",
        ).execute()
        resources = [ r for r in resources if r["Ident"] in choices]

    results = []

    ec2_resources = [ r for r in resources if r["Kind"] == "ec2" ]
    results += ec2.run_command(ec2_resources, command)

    ecs_resources = [ r for r in resources if r["Kind"] == "ecs" ]
    results += ecs.run_command(ecs_resources, command)

    success = True
    for result in results:
        print( _get_result_output(result) )
        if result["Status"] != "Success":
            success = False

    if not success:
        sys.exit(1)
