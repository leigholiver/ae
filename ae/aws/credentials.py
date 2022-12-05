import json
import os
import stat
import time

from .. import config, __base_path__
from . import session

_credentials = {}
_credentials_file = None

def _expired(credentials):
    return credentials["expiry"] <= time.time()

def credentials(role=None):
    if role:
        creds = from_role( role )
    else:
        creds = from_session( session.session(role) )

    return {
        "AWS_ACCESS_KEY_ID": creds["AccessKeyId"],
        "AWS_SECRET_ACCESS_KEY": creds["SecretAccessKey"],
        "AWS_SESSION_TOKEN": creds["SessionToken"],
        "AWS_SECURITY_TOKEN": creds["SessionToken"],
        "AWS_REGION": creds["region"],
    }

def from_session(session):
    creds = session.get_credentials()
    return {
        "AccessKeyId": creds.access_key,
        "SecretAccessKey": creds.secret_key,
        "SessionToken": creds.token if creds.token else '',
        "region": session.region_name
    }

def from_role(role):
    _setup_credentials()
    role_data = config.get(f"roles.{role}", None)
    if not role_data:
        raise Exception(f"Unknown role {role}")

    # do we have credentials for the role already?
    if role in _credentials.keys() and not _expired(_credentials[role]):
        return _credentials[role]

    if "region" not in role_data.keys():
        role_data["region"] = config.get("aws-region")

    sts = session.client("sts")
    session_duration = config.get("session.duration", 900)
    response = sts.assume_role(
        RoleArn=role_data["arn"],
        RoleSessionName=config.get("session.name", "ae-aws-extended"),
        DurationSeconds=session_duration
    )

    _credentials[role] = {
        "AccessKeyId": response["Credentials"]["AccessKeyId"],
        "SecretAccessKey": response["Credentials"]["SecretAccessKey"],
        "SessionToken": response["Credentials"]["SessionToken"],
        "region": role_data["region"],
        "expiry": time.time() + session_duration
    }
    _save_credentials()
    return _credentials[role]


def _setup_credentials():
    global _credentials_file
    global _credentials

    if not _credentials_file:
        _credentials_file = f"{__base_path__}/{config.get('name', 'default')}/credentials.json"

    if not os.path.isfile(_credentials_file) or _credentials != {}:
        return

    with open(_credentials_file, "r") as file:
        _credentials = json.load(file)

def _save_credentials():
    if not config.get('cache-credentials', True):
        return

    global _credentials_file
    with open(_credentials_file, "w") as f:
        f.write(json.dumps(_credentials))

    # Ensure only readable by current-user
    os.chmod(
        _credentials_file,
        stat.S_IRUSR |
        stat.S_IWUSR
    )
