import json
import subprocess
from os.path import basename
from google.cloud import storage

BUCKET_NAME = "my_test_bucket_333"
gcs_client = storage.Client()


def run_simulation(request):
    input_json = request.get_json()
    with open("/tmp/input.json", "w+") as f:
        json.dump(input_json, f)

    sim_gcs_path = input_json["sim_gcs_path"]
    sim_filename = basename(sim_gcs_path)

    bucket = gcs_client.get_bucket(BUCKET_NAME)

    blob = bucket.blob(sim_gcs_path)
    blob.download_to_filename(f"/tmp/{sim_filename}")

    subprocess.run(["python3", f"/tmp/{sim_filename}", "/tmp/input.json"])

    with open("/tmp/output.json") as f:
        result = json.load(f)
    result["run_id"] = input_json["run_id"]

    return result
