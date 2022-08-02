from pathlib import Path

from google.cloud import storage


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


def get_relative_filepaths(directory):
    filepaths = list(Path(directory).glob("*.json"))
    filepaths.sort(key=lambda path: (len(path.name), path.name))

    return filepaths
