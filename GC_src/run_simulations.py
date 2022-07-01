import subprocess
from google.cloud import storage
import json
from os.path import basename, exists

BUCKET_NAME = "cloudvvuq"
gcs_client = storage.Client()


def run_simulation(request):
    input_json = request.get_json()
    input_path = f"/tmp/input_{input_json['input_id']}.json"
    input_json["outfile"] = f"/tmp/output_{input_json['input_id']}.json"

    with open(input_path, "w+") as f:
        json.dump(input_json, f)

    sim_gcs_path = input_json["sim_gcs_path"]
    sim_filename = basename(sim_gcs_path)
    sim_path = f"/tmp/{sim_filename}"

    if not exists(sim_path):
        bucket = gcs_client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(sim_gcs_path)
        blob.download_to_filename(sim_path)

    subprocess.run(["python3", sim_path, input_path])

    with open(input_json["outfile"]) as f:
        result = json.load(f)

    result.update(input_json)

    return result
