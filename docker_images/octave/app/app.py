import os
import subprocess
from os.path import basename, exists

from scipy.io import savemat, loadmat
from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)

BUCKET_NAME = "cloudvvuq"
gcs_client = storage.Client()


@app.route("/", methods=["POST"])
def run_script():
    input_json = request.get_json()

    input_file = os.path.join(input_dir, f"input_{input_json['run_id']}.mat")
    output_file = os.path.join(output_dir, f"output_{input_json['run_id']}.mat")

    sim_gcs_path = input_json["sim_gcs_path"]
    sim_filename = basename(sim_gcs_path)
    sim_path = f"/tmp/{sim_filename}"

    if not exists(sim_path):
        bucket = gcs_client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(sim_gcs_path)
        blob.download_to_filename(sim_path)

    savemat(input_file, input_json)

    subprocess.run(["octave", sim_path, input_file, output_file, "--no-gui", "--silent"])

    result = loadmat(output_file)

    result = {k: v.item() for k, v in result.items()}
    result.update(input_json)

    return result


if __name__ == "__main__":
    input_dir = "/tmp/inputs"
    output_dir = "/tmp/outputs"
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    app.run(debug=False, host="0.0.0.0", port=8080)
