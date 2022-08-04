import json

import cachetools.func

import google.auth.transport.requests
import google.oauth2.id_token
from botocore import session, awsrequest, auth


class Authorizer:
    AWS_CREDENTIALS = session.Session().get_credentials()
    url: str
    cloud_provider: str

    def __init__(self, url: str,  cloud_provider: str):
        self.url = url
        self.cloud_provider = cloud_provider

    def sign_request(self, payload):
        if self.cloud_provider == "aws":
            return self.aws_sign_headers(self.url, payload)
        elif self.cloud_provider == "gcp":
            return {"Authorization": f"Bearer {self.get_gcp_token(self.url)}"}
        else:
            raise ValueError("Unknown provider")

    def aws_sign_headers(self, url: str, payload: dict):
        service = "lambda"
        region = url.split('.')[-3]
        request = awsrequest.AWSRequest(method='POST', url=url, data=json.dumps(payload))

        auth.SigV4Auth(Authorizer.AWS_CREDENTIALS, service, region).add_auth(request)

        return dict(request.headers.items())

    @cachetools.func.ttl_cache(ttl=3200)
    def get_gcp_token(self, audience: str):  # lifetime 1h
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)
        return id_token
