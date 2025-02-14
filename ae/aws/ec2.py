import json
import time

from . import session
from .. import shell
from .. import resources


def describe_running_instances(role=None, filters=[]):
    filters += [{"Name": "instance-state-name", "Values": ["running"]}]
    return describe_instances(role, filters)


def describe_instances(role=None, filters=[]):

    client = session.client("ec2", role)

    instances = []
    next_token = ""
    while True:
        response = client.describe_instances(Filters=filters, NextToken=next_token)
        for res in response["Reservations"]:
            for i in res["Instances"]:
                i["Tags"] = (
                    {tag["Key"]: tag["Value"] for tag in i["Tags"]}
                    if "Tags" in i.keys()
                    else {}
                )
                i["Name"] = i["Tags"].get("Name")
                i["Role"] = role
                i["Kind"] = "ec2"

                i["Ident"] = resources.build_ident(
                    i, unique_id=i["InstanceId"].replace("-", ""), role=role
                )
                instances.append(i)

        if "NextToken" not in response.keys():
            break

        next_token = response["NextToken"]

    return instances


def connect(instance):
    shell.run(
        ["aws", "ssm", "start-session", "--target", instance["InstanceId"]],
        role=instance["Role"],
    )


def port_forward(instance, local_port, remote_port):
    shell.run(
        [
            "aws",
            "ssm",
            "start-session",
            "--target",
            instance["InstanceId"],
            "--document-name",
            "AWS-StartPortForwardingSession",
            "--parameters",
            json.dumps(
                {
                    "localPortNumber": [str(local_port)],
                    "portNumber": [str(remote_port)],
                }
            ),
        ],
        role=instance["Role"],
    )


def run_command(instances, command):

    for instance in instances:
        ssm = session.client("ssm", instance["Role"])

        response = ssm.send_command(
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": [command]},
            InstanceIds=[instance["InstanceId"]],
        )

        # wait for the command to complete...
        complete = False
        while not complete:
            time.sleep(1)

            status_response = ssm.get_command_invocation(
                CommandId=response["Command"]["CommandId"],
                InstanceId=instance["InstanceId"],
            )

            if status_response["Status"] not in ["InProgress", "Pending"]:
                complete = True
                yield {
                    "Ident": instance["Ident"],
                    "Status": status_response["Status"],
                    "StdOut": status_response["StandardOutputContent"],
                    "StdErr": status_response["StandardErrorContent"],
                }
