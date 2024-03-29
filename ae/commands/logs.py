import click
import time

from colorama import Fore
from .. import ae
from ..decorators import find_resources_multi
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
@click.argument("log_groups", nargs=-1)
@find_resources_multi("log_groups", kinds=["logs"])
def logs_cmd(follow, since, log_groups):
    start_time = ( int(time.time()) - (since * 60) ) * 1000

    clients = {}
    for log_group in log_groups:
        clients[log_group["Ident"]] = session.client("logs", log_group["Role"])

    while True:
        events = []
        for log_group in log_groups:
            events += _get_logs(clients[log_group["Ident"]], log_group, start_time)

        if len(events) > 0:
            events = sorted(events, key=lambda e: e["timestamp"])
            start_time = events[-1]["timestamp"]

            for event in events:
                msg = event['message']
                if len(log_groups) > 1:
                    msg = f"{_get_styled_name(event['logStreamName'])} | {event['message']}"

                click.echo(msg)

        if not follow:
            break

        time.sleep(5)

def _get_logs(client, log_group, start_time, end_time=None):

    if not end_time:
        end_time = int(time.time()) * 1000

    events = []
    kwargs = {
        "logGroupName": log_group["logGroupName"],
        "startTime": start_time + 1,
        "endTime": end_time,
    }
    while True:
        response = client.filter_log_events(**kwargs)
        for event in response["events"]:
            events.append(event)

        if "nextToken" not in response.keys():
            break

        kwargs["nextToken"] = response["nextToken"]

    return events

_colors = [
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'bright_green',
    'bright_yellow',
    'bright_blue',
    'bright_magenta',
    'bright_cyan',
]
_name_colors = {}
def _get_styled_name(logStreamName):
    global _colors
    global _name_colors

    name = logStreamName.split('/')[0]
    if name not in _name_colors.keys():
        _name_colors[name] = _colors[ len(_name_colors) % len(_colors) ]

    return click.style(f"{name: >25}", fg=_name_colors[name], bold=True)
