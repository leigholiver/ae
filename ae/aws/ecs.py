import json

from .. import resources
from . import session
from .. import shell

def describe_tasks(role=None):

    client = session.client("ecs", role)
    cluster_arns = client.list_clusters()
    tasks = []
    for cluster in cluster_arns["clusterArns"]:
        task_arns = client.list_tasks(
            cluster=cluster,
            desiredStatus="RUNNING"
        )

        if task_arns["taskArns"] == []:
            continue

        response = client.describe_tasks(
            cluster=cluster,
            tasks=task_arns["taskArns"],
            include=["TAGS"]
        )

        for t in response["tasks"]:
            if t["lastStatus"] != "RUNNING":
                continue

            t["tags"] = { tag["key"]: tag["value"] for tag in t["tags"] } if "tags" in t.keys() else {}

            # we can get these from ecs managed tags, but only works on EC2 launch type
            # to rely on them later on, we set the expected tags
            cluster_name = "".join(t["clusterArn"].split("/")[1:])
            service_name = t['group'].replace("service:", "")
            t['tags']['aws:ecs:clusterName'] = cluster_name
            t['tags']['aws:ecs:serviceName'] = service_name

            t["Name"] = service_name
            t["Role"] = role
            t["Kind"] = "ecs"
            t["Id"] = t["taskArn"].split("/")[-1]

            if len(t['containers']) == 1:
                t["Ident"] = resources.build_ident(
                    t,
                    unique_id=t["Id"],
                    role=role
                )

                # You can use this to use some of the EC2 SSM functions - https://stackoverflow.com/a/67641633
                if 'runtimeId' in t['containers'][0].keys():
                    t["InstanceId"] = f"ecs:{cluster_name}_{t['Id']}_{t['containers'][0]['runtimeId']}"
                tasks.append(t)

            else:
                for c in t['containers']:
                    # clone the task so that we can create a resource-per-container
                    current = t.copy()

                    # remove the other containers
                    current["containers"] = [c]

                    current["Ident"] = f"{c['name']}-"
                    current["Ident"] += resources.build_ident(
                        current,
                        unique_id=current["Id"],
                        role=role
                    )

                    # You can use this to use some of the EC2 SSM functions - https://stackoverflow.com/a/67641633
                    if 'runtimeId' in c.keys():
                        current["InstanceId"] = f"ecs:{cluster_name}_{current['Id']}_{c['runtimeId']}"
                    tasks.append(current)

    return tasks

def ecs_exec(instance, command="/bin/sh"):
    return [
        "aws", "ecs", "execute-command",
        "--cluster", instance["tags"]["aws:ecs:clusterName"],
        "--task", instance["Id"],
        "--container", instance["containers"][0]["name"],
        "--interactive",
        "--command", command
    ]

def connect(instance):
    shell.run(
        ecs_exec(instance),
        role=instance["Role"],
    )

def run_command(instances, command):

    # Some nasty stuff here, to get ecs-exec to report a failure with exit code/status correctly
    wrapped_cmd = f"sh -c 'sh -c \"{command}\"; echo $?'"

    for instance in instances:
        output = shell.run(
            ecs_exec(instance, wrapped_cmd),
            role=instance["Role"],
            interactive=False
        )
        output_lines = output.split("\n")
        output = "\n".join(output_lines[5:-6])
        status = output_lines[-6].replace("\r", "")

        yield {
            "Ident": instance["Ident"],
            "Status": "Success" if status == "0" else "Failed",
            "StdOut": output,
            "StdErr": f"failed to run commands: exit status {status}" if status != "0" else "",
        }
