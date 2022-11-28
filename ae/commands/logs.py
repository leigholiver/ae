import click
import time

from .. import ae
from ..decorators import find_resources
from ..aws import session

description = """\b
Show logs from a Cloudwatch log group
"""

@ae.command(
    name="logs",
    aliases=["l"],
    help=description
)
@click.option(
    '--follow',
    '-f',
    is_flag=True,
    default=False,
    help='Check for, and append new logs'
)
@click.option(
    '--since',
    '-s',
    default=5,
    type=int,
    help='Time in minutes to get logs since (default 5)'
)
@click.argument("log_group")
@find_resources("log_group", kinds=["logs"])
def logs_cmd(follow, since, log_group):

    client = session.client("logs", log_group["Role"])
    start_time = ( int(time.time()) - (since * 60) ) * 1000

    while True:
        events = _get_logs(client, log_group, start_time)

        for event in events:
            if event["timestamp"] > start_time:
                start_time = event["timestamp"]
            print(event["message"])

        if not follow:
            break

        time.sleep(5)

def _get_logs(client, lg, start_time, end_time=None):

    if not end_time:
        end_time = int(time.time()) * 1000

    events = []
    kwargs = {
        "logGroupName": lg["logGroupName"],
        "startTime": start_time,
        "endTime": end_time,
    }
    while True:
        response = client.filter_log_events(**kwargs)
        for event in response["events"]:
            yield event

        if "nextToken" not in response.keys():
            break

        kwargs["nextToken"] = response["nextToken"]

    return events
