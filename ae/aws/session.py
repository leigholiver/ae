import boto3
import time
import threading

from .. import config
from . import credentials

_sessions = {}

# name of all sessions, including "None" - the root session
def names():
    return [None] + list(config.get("roles", {}).keys())

def client(service, role=None):
    return session(role).client(service)

def session(role=None):
    global _sessions

    # If this thread does not already have a session cache, create one
    thread_id = threading.get_ident()
    if thread_id not in _sessions.keys():
         _sessions[thread_id] = {}

    # Tag the root session so that it has a key...
    name = "ae-root-session" if not role else role

    # If we already have a session, return it
    if name in _sessions[thread_id].keys():
        return _sessions[thread_id][name]

    if role:
        kwargs = _assume_role(role)
    else:
        kwargs = {
            "region_name": config.get("aws-region"),
            "profile_name": config.get("aws-profile"),
        }

    output = boto3.session.Session(**kwargs)
    _sessions[thread_id][name] = output
    return output

def _assume_role(role):
    creds = credentials.from_role(role)

    return {
        "aws_access_key_id": creds["AccessKeyId"],
        "aws_secret_access_key": creds["SecretAccessKey"],
        "aws_session_token": creds["SessionToken"],
        "region_name": creds["region"],
    }
