# https://aws.amazon.com/blogs/database/get-started-with-amazon-elasticsearch-service-an-easy-way-to-send-aws-sigv4-signed-requests/
import boto3
import requests
from requests_aws4auth import AWS4Auth

from . import session

def send_signed(method, url, service='es', region='eu-west-1', body=None, role=None):
    credentials = session.session(role).get_credentials()
    auth = AWS4Auth(credentials.access_key, credentials.secret_key,
                  region, service, session_token=credentials.token)

    fn = getattr(requests, method)
    if body and not body.endswith("\n"):
        body += "\n"

    return fn(url, auth=auth, data=body,
       headers={"Content-Type":"application/json"})
