import time
import json
from pathlib import Path

from tqdm import tqdm

from cloudvvuq.cloud_connector import CloudConnector


class Executor:
    url: str
    work_dir: Path

    def __init__(self, url: str, work_dir: [Path, str] = None):
        self.url = url
        self.work_dir = Path(work_dir) if work_dir else Path(Path(__file__).resolve().parents[1], "runs",
                                                             f"run_{int(time.time())}")

    def _prepare_samples(self, samples: list):
        for i, sample in enumerate(samples):
            sample["input_id"] = i

        return samples

    def _run(self, inputs: list, *, batch_size: int = 0, require_auth: bool = True):
        if batch_size == 0:
            batch_size = len(inputs)

        results = []
        batches = tqdm(range(0, len(inputs), batch_size),
                       bar_format='Total progress: {l_bar}{bar:10}{r_bar}{bar:-10b}')

        connector = CloudConnector(self.url, self.work_dir, require_auth)

        for batch in batches:
            input_batch = inputs[batch:batch + batch_size]
            results_batch = connector.send_and_receive(input_batch, pbar=batches)
            results.extend(results_batch)

        return results

    def run(self, samples: list, *, batch_size: int = 0, require_auth: bool = True):
        inputs = self._prepare_samples(samples)
        self.save_run_inputs(inputs)

        results = self._run(inputs, batch_size=batch_size, require_auth=require_auth)

        return results

    def rerun_missing(self, batch_size: int = 0, require_auth: bool = True):

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
            output_path = Path(outputs_dir, f"output_{input_id}")
            if not output_path.exists():
                input_path = Path(inputs_dir, input_file)
                with open(input_path) as f:
                    inputs_without_outputs.append(json.load(f))

        self._run(inputs_without_outputs, batch_size=batch_size, require_auth=require_auth)

    def save_run_inputs(self, inputs: list, save_dir: [Path, str] = None):
        save_dir = Path(save_dir) if save_dir else Path(self.work_dir, "inputs")
        save_dir.mkdir(parents=True, exist_ok=True)

        for input in inputs:
            output_path = Path(save_dir, f"input_{input['input_id']}.json")
            with open(output_path, "w+") as f:
                json.dump(input, f, indent=4)
