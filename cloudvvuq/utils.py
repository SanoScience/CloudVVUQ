import os

import google.oauth2.id_token
import google.auth.transport.requests
from google.cloud import storage


def get_token(audience):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)
    return id_token


def upload_files(files):
    BUCKET_NAME = "cloudvvuq"
    gcs_client = storage.Client()

    bucket = gcs_client.get_bucket(BUCKET_NAME)
    gcs_paths = []
    for file in files:
        filename = os.path.basename(file)
        path = f"inputs/{filename}"

        blob = bucket.blob(path)
        blob.upload_from_filename(file)

        gcs_paths.append(path)

    return gcs_paths


def absolute_filepaths(directory):
    filepaths = []
    for dir_path, _, filenames in os.walk(directory):
        for f in filenames:
            abs_filepath = os.path.abspath(os.path.join(dir_path, f))
            filepaths.append(abs_filepath)

    filepaths.sort(key=lambda path: (len(path), path))
    return filepaths
