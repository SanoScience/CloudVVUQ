import os
import json
import subprocess


def lambda_handler(event, context):
    input_json = json.loads(event['body'])
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

    return {
        "statusCode": 200,
        "body": json.dumps(result),
        "headers": {
            "content-type": "application/json"
        },
        "isBase64Encoded": False
    }
