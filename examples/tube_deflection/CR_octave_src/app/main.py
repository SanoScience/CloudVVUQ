import os
import subprocess

from scipy.io import savemat, loadmat
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def run_script():
    input_json = request.get_json()

    input_file = f"/tmp/input_{input_json['input_id']}.mat"
    output_file = f"/tmp/output_{input_json['input_id']}.mat"

    savemat(input_file, input_json)

    subprocess.run(["octave", "tube_deflection.m", input_file, output_file, "--no-gui", "--silent"])

    result = loadmat(output_file)

    result = {k: v.item() for k, v in result.items()}
    result.update(input_json)

    os.remove(input_file)
    os.remove(output_file)

    return result


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
