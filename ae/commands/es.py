import click
import sys
import json

from .. import ae
from ..decorators import find_resources
from ..aws import signing

description = """\b
Send a signed request to an opensearch url
"""

@ae.command(
    name="es",
    help=description
)
@click.argument("resource", required=True)
@click.argument("method", type=click.Choice(['GET', 'PUT', 'POST', 'PATCH', 'DELETE']), required=True)
@click.argument("path", required=True)
@click.argument("body", required=False)
@click.option("--region", default='eu-west-1')
@find_resources("resource", kinds=["es"])
def es(resource, path, method, body, region):
    response = signing.send_signed(method.lower(), f"https://{resource['Endpoint']}{path}", 'es', region, body, resource['Role'])

    # print the status code to stderr so that we can still pipe it into jq etc
    print(f"Status code: {response.status_code}", file=sys.stderr)

    # pretty print the response if its JSON
    if "application/json" in response.headers['Content-Type']:
        print(json.dumps(response.json(), indent=2))
    else:
        print(response.text)
