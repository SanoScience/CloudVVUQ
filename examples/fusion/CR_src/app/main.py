import os
import json
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def run_script():
    input_json = request.get_json()
    input_file = os.path.join(input_dir, f"input_{input_json['input_id']}.json")
    input_json["outfile"] = os.path.join(output_dir, f"output_{input_json['input_id']}.json")

    with open(input_file, "w+") as f:
        json.dump(input_json, f)

    subprocess.run(["python3", "fusion.py", input_file], capture_output=True)

    with open(input_json["outfile"]) as f:
        result = json.load(f)

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
