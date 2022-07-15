import os
import json
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def run_script():
    input_json = request.get_json()
    input_file = f"/tmp/input_{input_json['input_id']}.json"
    input_json["outfile"] = f"/tmp/output_{input_json['input_id']}.json"

    with open(input_file, "w+") as f:
        json.dump(input_json, f)

    subprocess.run(["python3", "beam.py", input_file], capture_output=True)

    with open(input_json["outfile"]) as f:
        result = json.load(f)

    result.update(input_json)

    os.remove(input_file)
    os.remove(input_json["outfile"])

    return result


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
