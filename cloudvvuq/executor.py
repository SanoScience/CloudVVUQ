import time
import json
import tempfile
from pathlib import Path

from cloudvvuq.cloud_connector import CloudConnector


class Executor:
    url: str
    work_dir: Path

    def __init__(self, url: str, work_dir: [Path, str] = None):
        self.url = url
        self.work_dir = Path(work_dir) if work_dir else Path(tempfile.gettempdir(), "CloudVVUQ_runs",
                                                             f"run_{int(time.time())}")

        self.work_dir.mkdir(parents=True, exist_ok=True)

    def _prepare_samples(self, samples: list[dict]):
        for i, sample in enumerate(samples):
            if "input_id" not in sample:
                sample["input_id"] = i

        return samples

    def _run(self, inputs: list[dict], *, max_load: int = 0, cloud_provider: str = None):
        if max_load == 0:
            max_load = len(inputs)

        connector = CloudConnector(self.url, self.work_dir, cloud_provider, max_load)
        results = connector.fetch_all(inputs)

        return results

    def run(self, samples: list[dict], *, max_load: int = 0, cloud_provider: str = None):
        inputs = self._prepare_samples(samples)
        self.save_run_inputs(inputs)

        results = self._run(inputs, max_load=max_load, cloud_provider=cloud_provider)

        return results

    def find_inputs_to_rerun(self):
        inputs_dir = Path(self.work_dir, "inputs")
        outputs_dir = Path(self.work_dir, "outputs")

        if not inputs_dir.exists():
            raise ValueError("Input directory not found.")
        if not outputs_dir.exists():
            raise ValueError("Output directory not found.")

        input_files = [input_json for input_json in Path(inputs_dir).glob("*.json")]
        inputs_without_outputs = []

        for input_file in input_files:
            input_id = input_file.stem.split("_")[-1]
            output_path = Path(outputs_dir, f"output_{input_id}.json")
            if not output_path.exists():
                input_path = Path(inputs_dir, input_file)
                with open(input_path) as f:
                    inputs_without_outputs.append(json.load(f))

        return inputs_without_outputs

    def save_run_inputs(self, inputs: list[dict], save_dir: [Path, str] = None):
        save_dir = Path(save_dir) if save_dir else Path(self.work_dir, "inputs")
        save_dir.mkdir(parents=True, exist_ok=True)

        for input in inputs:
            output_path = Path(save_dir, f"input_{input['input_id']}.json")
            if output_path.exists():
                continue
            with open(output_path, "w+") as f:
                json.dump(input, f, indent=4)
