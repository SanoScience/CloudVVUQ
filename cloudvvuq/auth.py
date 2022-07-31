import json

import google.auth.transport.requests
import google.oauth2.id_token
from botocore import session, awsrequest, auth

AWS_CREDENTIALS = session.Session().get_credentials()


def get_gcp_token(audience):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)
    return id_token


def aws_sign_headers(url: str, payload: dict):
    service = "lambda"
    region = url.split('.')[-3]
    request = awsrequest.AWSRequest(method='POST', url=url, data=json.dumps(payload))

    auth.SigV4Auth(AWS_CREDENTIALS, service, region).add_auth(request)

    return dict(request.headers.items())
