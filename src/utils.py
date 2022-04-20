import os

import google.oauth2.id_token
import google.auth.transport.requests
from google.cloud import storage


def get_token(audience):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)
    return id_token


def upload_files(files):
    BUCKET_NAME = "my_test_bucket_333"  # todo create new bucket with good name
    gcs_client = storage.Client()

    bucket = gcs_client.get_bucket(BUCKET_NAME)
    gcs_paths = []
    for file in files:
        filename = os.path.basename(file)
        path = f"inputs/{filename}"  # todo group input files

        blob = bucket.blob(path)
        blob.upload_from_filename(file)

        gcs_paths.append(path)

    return gcs_paths


def absoluteFilePaths(directory):
    for dir_path, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dir_path, f))
