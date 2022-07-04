import json
import subprocess


def run_script(request):
    input_json = request.get_json()
    input_file = f"/tmp/input_{input_json['input_id']}.json"
    input_json["outfile"] = f"/tmp/output_{input_json['input_id']}.json"

    with open(input_file, "w+") as f:
        json.dump(input_json, f)

    subprocess.run(["python3", "ishigami.py", input_file])

    with open(input_json["outfile"]) as f:
        result = json.load(f)

    result.update(input_json)

    return result
