## Choosing deployment type

In order to successfully deploy your model for CloudVVUQ usage you must consider few aspects:

- Available services to you
- Source code language
    - Services such as Google Cloud Functions do not support every language as runtime. If your code is written in e.g. Octave you have to use services that support running custom container images.  
- Maximum execution time of your model
    - If you deploy a model which takes 30 min to compute you should not use AWS Lambda but Google Cloud Run instead. More about the service-specific quotas in cloud configuration section.
- Dependencies
    - If you need to package custom software or dependencies along the model's source code container image is your best option as deployment type.


## Model preparation

In this step we assume you have a working computational model.  

To prepare the model for deployment you must:  

  - specify requirements and dependencies  
  - support execution of the model which takes path to a json-file with model arguments/samples and saves results to json-file  

For the 2nd step provide a command-line interface for your model such as:  
  ```bash
  python3 model.py input_file.json
  ```
  Your model.py file must take one argument - input_file which is a path to file with your sample's values packed in json.

  Below is copy-ready code (in Python).
  ```python
  import sys
  import json
  
  json_input = sys.argv[1]
  with open(json_input, 'r') as fd:
      inputs = json.load(fd)
  ``` 
  Then you have to unpack the values in before you pass them into the model e.g.:
  ```python
  F = inputs['F']
  L = inputs['L']
  a = inputs['a']
  D = inputs['D']
  ```
  Then you can pass the variables into your model execution function.
  ```python
  g1, g2, g3 = solve_sample(F, L, a, D)
  ```  
  After the model has been solved you return the results. You can do this like this:
  ```python
  with open(inputs['outfile'], 'w') as fd:
      json.dump({'g1': g1, 'g2': g2, 'g3': g3}, fd)
  ```

This is simple communication by file. The parent-process passes the filepath to child-process. Child process reads the sample's values from the file, executes the model with those values and returns the results to the parent in another file. The parent then sends back the response with model outputs to the client.  
 
Alternatively if your model is written in Python you can import the interface method in the "server" code
  ```python
  output = model_solve_sample(inputs)
  ```
  This way you can skip the communication by files. Also, you slightly reduce the execution time because you don't start and new process but reuse existing one. Noticeable difference only for very fast models (<1s).
  
## Wrapper code ("server" code)

Each service requires slightly different wrapper code. Here are boilerplate code for each service. Reuse existing code are replace the 'model.py' with relative path to your model's code.
#### AWS Lambda - layers
```python
import json
import subprocess


def lambda_handler(event, context):
    input_json = event['body']  # extract sample
    input_file = f"/tmp/input_{input_json['input_id']}.json"  
    input_json["outfile"] = f"/tmp/output_{input_json['input_id']}.json"  # add outfile path to sample dict

    with open(input_file, "w+") as f:  # save sample to file
        json.dump(input_json, f)

    subprocess.run(["python3", "model.py", input_file])  # start a new process with model computation and pass sample 

    with open(input_json["outfile"]) as f:  # read results from output file
        result = json.load(f)

    result.update(input_json) 

    return result  # return model outputs to the client

```

#### AWS Lambda - image
```python
import json
import subprocess


def lambda_handler(event, context):
    input_json = json.loads(event['body'])
    input_file = f"/tmp/input_{input_json['input_id']}.json"
    input_json["outfile"] = f"/tmp/output_{input_json['input_id']}.json"

    with open(input_file, "w+") as f:
        json.dump(input_json, f)

    subprocess.run(["python3", "model.py", input_file])

    with open(input_json["outfile"]) as f:
        result = json.load(f)

    result.update(input_json)

    return {
        "statusCode": 200,
        "body": json.dumps(result),
        "headers": {
            "content-type": "application/json"
        },
        "isBase64Encoded": False
    }

```

#### Google Cloud Run
```python
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

    subprocess.run(["python3", "model.py", input_file], capture_output=True)

    with open(input_json["outfile"]) as f:
        result = json.load(f)

    result.update(input_json)

    os.remove(input_file)
    os.remove(input_json["outfile"])

    return result


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

```

#### Google Cloud Functions
```python
import json
import subprocess


def run_script(request):
    input_json = request.get_json()
    input_file = f"/tmp/input_{input_json['input_id']}.json"
    input_json["outfile"] = f"/tmp/output_{input_json['input_id']}.json"

    with open(input_file, "w+") as f:
        json.dump(input_json, f)

    subprocess.run(["python3", "model.py", input_file])

    with open(input_json["outfile"]) as f:
        result = json.load(f)

    result.update(input_json)

    return result

```
