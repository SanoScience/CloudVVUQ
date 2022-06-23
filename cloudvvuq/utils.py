import os

import google.oauth2.id_token
import google.auth.transport.requests
from google.cloud import storage


def get_gcp_token(audience):
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)
    return id_token


def upload_files(files, bucket_name):
    gcs_client = storage.Client()

    bucket = gcs_client.get_bucket(bucket_name)
    gcs_paths = []
    for file in files:
        filename = os.path.basename(file)
        path = f"inputs/{filename}"

        blob = bucket.blob(path)
        blob.upload_from_filename(file)

        gcs_paths.append(path)

    return gcs_paths


def relative_filepaths(directory):
    filepaths = [os.path.join(directory, f).replace("/", os.sep).replace("\\", os.sep)  # todo move to pathlib?
                 for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    filepaths.sort(key=lambda path: (len(path), path))
    return filepaths
