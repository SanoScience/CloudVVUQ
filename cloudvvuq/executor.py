import time
import json
import asyncio
from pathlib import Path

import easyvvuq as uq
from tqdm import tqdm

from cloudvvuq.async_utlis import run_simulations
from cloudvvuq.utils import get_relative_filepaths


class Executor:
    # Cloud
    url: str

    # Sampler
    sampler: uq.sampling
    params: dict

    # Local
    work_dir: Path

    def __init__(self, url: str, work_dir: [Path, str] = None):
        self.url = url
        self.work_dir = Path(work_dir) if work_dir else Path(Path(__file__).resolve().parents[1], "runs",
                                                             f"run_{int(time.time())}")

    def set_sampler(self, sampler: uq.sampling, params: dict):
        self.sampler = sampler
        self.params = params

    def _find_max_samples(self, n_samples):
        """
        Find max number of samples for current sampler and update n_samples if is lower or n_samples == 0.
        :param n_samples: User defined number of samples
        :return: min(n_samples, sampler_max_samples) or (sampler_max_samples if n_samples == 0)
        """
        if hasattr(self.sampler, "n_samples"):
            if isinstance(self.sampler.n_samples, int):
                sampler_max_samples = self.sampler.n_samples
            elif callable(self.sampler.n_samples):
                try:
                    sampler_max_samples = self.sampler.n_samples()
                except RuntimeError:  # Infinite samples
                    return n_samples
            else:
                return n_samples

            if n_samples == 0:
                return sampler_max_samples
            else:
                return min(n_samples, sampler_max_samples)

        return n_samples

    def draw_samples(self, n_samples: int = 0):
        if self.sampler is None or self.params is None:
            raise ValueError("Sampler or its arguments are not set, use set_sampler method before drawing samples")

        if not self.sampler.is_finite() and n_samples == 0:
            msg = (f"Sampling_element '{self.sampler.element_name()}' "
                   f"is an infinite generator, therefore a finite number of "
                   f"draws (n > 0) must be specified.")
            raise RuntimeError(msg)

        new_runs = []
        num_added = 0
        n_samples = self._find_max_samples(n_samples)

        for run in tqdm(self.sampler, total=n_samples, desc="Sampling ...  "):
            if num_added >= n_samples:
                break

            missing_params = [param for param in self.params.keys() if param not in run.keys()]

            for param in missing_params:
                if "default" not in self.params[param]:
                    raise ValueError(f"Missing 'default' field in params for {param}")

                default_val = self.params[param]["default"]
                run[param] = default_val

            num_added += 1
            new_runs.append(run)

        return new_runs

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

        for batch in batches:
            input_batch = inputs[batch:batch + batch_size]
            results_batch = asyncio.run(run_simulations(input_batch, self.url, require_auth, pbar=batches))
            results.extend(results_batch)

        return results

    def run(self, samples: list, *, batch_size: int = 0, require_auth: bool = True):
        inputs = self._prepare_samples(samples)
        self.save_run_inputs(inputs)

        results = self._run(inputs, batch_size=batch_size, require_auth=require_auth)

        self.save_run_outputs(results)

        return results

    def rerun_missing(self, inputs_dir: [Path, str] = None, outputs_dir: [Path, str] = None, batch_size: int = 0,
                      require_auth: bool = True):

        inputs_dir = Path(inputs_dir) if inputs_dir else Path(self.work_dir, "inputs")
        outputs_dir = Path(outputs_dir) if outputs_dir else Path(self.work_dir, "outputs")

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

        results = self._run(inputs_without_outputs, batch_size=batch_size, require_auth=require_auth)

        self.save_run_outputs(results, outputs_dir)

    def save_run_inputs(self, inputs: list, save_dir: [Path, str] = None):
        save_dir = Path(save_dir) if save_dir else Path(self.work_dir, "inputs")
        save_dir.mkdir(parents=True, exist_ok=True)

        for input in inputs:
            output_path = Path(save_dir, f"input_{input['input_id']}.json")
            with open(output_path, "w+") as f:
                json.dump(input, f, indent=4)

    def save_run_outputs(self, results: list, save_dir: [Path, str] = None):
        save_dir = Path(save_dir) if save_dir else Path(self.work_dir, "outputs")
        save_dir.mkdir(parents=True, exist_ok=True)

        for result in results:
            output_path = Path(save_dir, f"output_{result['input_id']}.json")
            with open(output_path, "w+") as f:
                json.dump(result, f, indent=4)

    def create_campaign(self, name: str, input_columns: list[str], output_columns: list[str],
                        inputs_dir: [Path, str] = None, outputs_dir: [Path, str] = None):

        self.work_dir.mkdir(parents=True, exist_ok=True)  # used when importing external runs into campaign

        campaign = uq.Campaign(name=name + "_", work_dir=self.work_dir)
        campaign.add_app(name=name, params=self.params)
        campaign.set_sampler(self.sampler)

        inputs_dir = Path(inputs_dir) if inputs_dir else Path(self.work_dir, "inputs")
        outputs_dir = Path(outputs_dir) if outputs_dir else Path(self.work_dir, "outputs")
        input_filepaths = get_relative_filepaths(inputs_dir)
        output_filepaths = get_relative_filepaths(outputs_dir)

        if not output_filepaths:
            raise FileNotFoundError("Output files not found")
        if len(output_filepaths) < len(input_filepaths):
            raise FileNotFoundError("Missing outputs, try running 'rerun_missing' method before.")

        input_decoder = uq.decoders.JSONDecoder(target_filename='_', output_columns=input_columns)
        output_decoder = uq.decoders.JSONDecoder(target_filename='_', output_columns=output_columns)

        campaign.add_external_runs(input_filepaths, output_filepaths, input_decoder, output_decoder)

        return campaign
