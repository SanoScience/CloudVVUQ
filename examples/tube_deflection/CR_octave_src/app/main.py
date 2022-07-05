import os
import subprocess

from scipy.io import savemat, loadmat
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def run_script():
    input_json = request.get_json()

    input_file = os.path.join(input_dir, f"input_{input_json['input_id']}.mat")
    output_file = os.path.join(output_dir, f"output_{input_json['input_id']}.mat")

    savemat(input_file, input_json)

    subprocess.run(["octave", "tube_deflection.m", input_file, output_file, "--no-gui", "--silent"])

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
