import os
import yaml
from functools import reduce
from configparser import ConfigParser

from . import __home__, __base_path__

_config = {}
_config_file = None

def get_path():
    global _config_file
    return _config_file

def get(key, default=None):
    global _config

    try:
        keys = key.split(".")
        output = reduce(lambda val, key: val.get(key) if val else default, keys, _config)
        if not output:
            return default
        return output
    except:
        return default

def load(aws_profile=None):
    config = {}

    config_file = f"{__base_path__}/ae.yml"
    if aws_profile:
        config_file = f"{__base_path__}/{aws_profile}.yml"
        config["name"] = aws_profile

    # load in the config file
    if os.path.isfile(config_file):
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)

    if "aws-profile" not in config.keys():
        config["aws-profile"] = aws_profile

    # parse the aws config file
    if "role-source-profile" in config.keys():
        aws_cfg = parse_aws_config(config["role-source-profile"])
        config["name"] = config["role-source-profile"]

    else:
        aws_cfg = parse_aws_config(config["aws-profile"])

    # set the region from the aws config if it isnt specified in the config file
    if "aws-region" not in config.keys() and "region" in aws_cfg.keys():
        config["aws-region"] = aws_cfg["region"]

    # if roles are specified, pull in the arns/regions from the aws config file
    if "roles" in config.keys():
        config["roles"] = { key: role for key, role in aws_cfg["roles"].items() if key in config["roles"] }

    # if ignore-roles are specified, pull in the other roles from the aws config file
    elif "ignore-roles" in config.keys():
        config["roles"] = { key: role for key, role in aws_cfg["roles"].items() if key not in config["ignore-roles"] }

    # otherwise, just pull in all of the roles
    else:
        config["roles"] = aws_cfg["roles"]

    global _config
    _config = config

    global _config_file
    _config_file = config_file


def parse_aws_config(aws_profile):
    parser = ConfigParser()
    parser.read(f"{__home__}/.aws/config")

    config = {
        "roles": {}
    }

    for section in parser.sections():
        data = parser[section]

        # if this section is our target aws profile, grab the region
        if (aws_profile == "default" and section == "default") or (section == f"profile {aws_profile}"):
            if "region" in data.keys():
                config["region"] = data["region"]

        # otherwise, if the target profile is the source profile for this profile, add the role info
        elif "source_profile" in data.keys() and data["source_profile"] == aws_profile:
            role = {}

            if "role_arn" in data.keys():
                role["arn"] = data["role_arn"]

            if "region" in data.keys():
                role["region"] = data["region"]

            role_name = section.replace("profile ", "")
            config["roles"][role_name] = role

    return config
