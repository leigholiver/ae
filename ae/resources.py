import json
import os
import time
from pathlib import Path

from . import __base_path__
from . import config
from . import parallel
from .aws import session
from .aws import ec2
from .aws import ecs
from .aws import logs

def build_ident(data, unique_id=None, role=None):
    output = data["Name"] if data["Name"] else ""
    if role:
        output += f"-{role}"

    if unique_id:
        output += f"-{unique_id}"

    return output

def find_kind(role, kind):
    profile = config.get("name", "default")
    cfg_path = config.get_path()
    if cfg_path:
        profile = os.path.splitext( os.path.basename(cfg_path) )[0]

    data_file = f"{__base_path__}/{profile}"
    if role:
        data_file += f"/{role}"
    data_file += f"/{kind}.json"

    if os.path.isfile(data_file):
        with open(data_file, "r") as file:
            cached = json.load(file)
            if "timestamp" in cached.keys():
                expired = (time.time() - cached["timestamp"]) >= config.get("cache-time", 60)
                if not expired:
                    return cached["resources"]

    resources = []
    match kind:
        case "ec2":
            resources = ec2.describe_running_instances(role)
        case "ecs":
            resources = ecs.describe_tasks(role)
        case "logs":
            resources = logs.describe_log_groups(role)
        case _:
            raise Exception(f"Cant find unknown resource kind {kind}")

    output_file = Path( os.path.dirname(data_file) )
    output_file.mkdir(parents=True, exist_ok=True)
    with open(data_file, "w") as file:
        json.dump(
            {
                "timestamp": time.time(),
                "resources": resources
            },
            file, indent=2, default=str
        )

    return resources

def find_resources(ident, kinds=[]):
    if not ident:
        ident = ""

    args = []
    for kind in kinds:
        for name in session.names():
            args.append([find_kind, name, kind])

    resources = parallel.run(args)
    return [ r for r in resources if ident in r["Ident"] ]
