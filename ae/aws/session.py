import boto3
import threading

from .. import config

_sessions = {}

def names():
    return [None] + list(config.get("roles", {}).keys())

def credentials(role=None):
    _session = session(role)
    creds = _session.get_credentials()

    return {
        "AWS_ACCESS_KEY_ID": creds.access_key,
        "AWS_SECRET_ACCESS_KEY": creds.secret_key,
        "AWS_SESSION_TOKEN": creds.token if creds.token else '',
        "AWS_SECURITY_TOKEN": creds.token if creds.token else '',
        "AWS_REGION": _session.region_name,
    }

def client(service, role=None):
    return session(role).client(service)

def session(role=None):
    thread_id = threading.get_ident()
    if thread_id not in _sessions.keys():
         _sessions[thread_id] = {}

    if not role:
        if "ae_root_session" not in _sessions[thread_id].keys():
            _sessions[thread_id]["ae_root_session"] = boto3.session.Session(
                region_name=config.get("aws-region"),
                profile_name=config.get("aws-profile")
            )
        return _sessions[thread_id]["ae_root_session"]

    role_data = config.get(f"roles.{role}", None)
    if not role_data:
        raise Exception(f"Unknown role {role}")

    if role not in _sessions[thread_id].keys():
        _sessions[thread_id][role] = _assume_role(role_data)
    return _sessions[thread_id][role]

def _assume_role(role):
    if "region" not in role.keys():
        role["region"] = config.get("aws-region")

    sts = client("sts")

    response = sts.assume_role(
        RoleArn=role["arn"],
        RoleSessionName=config.get("session.name", "ae-aws-extended"),
        DurationSeconds=config.get("session.duration", 900)
    )

    return boto3.session.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
        region_name=role["region"]
    )
