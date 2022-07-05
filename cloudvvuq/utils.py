from pathlib import Path

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
        filename = Path(file).stem
        path = f"inputs/{filename}"

        blob = bucket.blob(path)
        blob.upload_from_filename(file)

        gcs_paths.append(path)

    return gcs_paths


def relative_filepaths(directory):
    filepaths = list(Path(directory).glob("*.json"))
    filepaths.sort(key=lambda path: (len(path.name), path.name))

    return filepaths


def batch_progress(curr, N, width=10, bars=u'▉▊▋▌▍▎▏ '[::-1],
                   full='█', empty=' '):
    p = curr / N
    nfull = int(p * width)
    return "Batch progress: {:>3.0%} |{}{}{}| {:>2}/{}" \
        .format(p, full * nfull,
                bars[int(len(bars) * ((p * width) % 1))] if curr != N else "",
                empty * (width - nfull - 1),
                curr, N)
