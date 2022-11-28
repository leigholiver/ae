from .. import resources
from . import session

def describe_log_groups(role=None):

    client = session.client("logs", role)

    log_groups = []
    kwargs = {}
    while True:
        response = client.describe_log_groups(**kwargs)
        for log_group in response["logGroups"]:
            log_group["Name"] = log_group["logGroupName"].split("/")[-1]
            log_group["Role"] = role
            log_group["Kind"] = "logs"
            log_group["Ident"] = resources.build_ident(
                log_group,
                role=role
            )
            log_groups.append(log_group)

        if "nextToken" not in response.keys():
            break

        kwargs["nextToken"] = response["nextToken"]

    return log_groups
