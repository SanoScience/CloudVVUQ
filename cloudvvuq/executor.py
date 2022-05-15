import os
import json

import time
import asyncio
import easyvvuq as uq

from cloudvvuq.async_utlis import run_simulations
from cloudvvuq.utils import absolute_filepaths


class Executor:
    # Cloud
    url: str
    sim_path: str  # todo add possibility to download and use additional files

    # Sampler
    sampler: uq.sampling
    params: dict

    # Local
    work_dir: str

    def __init__(self, url: str, sim_path: str, work_dir: str = None):
        self.url = url
        self.sim_path = sim_path
        self.work_dir = work_dir or os.path.join(os.path.dirname(__file__), "..", "runs", f"run_{int(time.time())}")
        # todo ^ what about jupyter usage, currently overwrites previous run_dirs

    def set_sampler(self, sampler: uq.sampling, params: dict):
        self.sampler = sampler
        self.params = params

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
        for run in self.sampler:
            missing_params = [param for param in self.params.keys() if param not in run.keys()]

            for param in missing_params:
                if "default" not in self.params[param]:
                    raise ValueError(f"Missing 'default' field in params for {param}")

                default_val = self.params[param]["default"]
                run[param] = default_val

            num_added += 1
            new_runs.append(run)

            if n_samples != 0 and num_added >= n_samples:
                break

        return new_runs

    def _prepare_samples(self, samples: list):
        paths = {"sim_gcs_path": self.sim_path}
        inputs = [{**input, **paths, "run_id": i, "outfile": f"/tmp/output_{i}.json"}
                  for i, input in enumerate(samples)]

        return inputs

    def run(self, samples: list):
        inputs = self._prepare_samples(samples)
        self.save_run_inputs(inputs)

        results = asyncio.run(run_simulations(inputs, self.url))

        self.save_run_outputs(results)

        return results

    def run_batch_mode(self, samples: list, batch_size: int):
        inputs = self._prepare_samples(samples)
        self.save_run_inputs(inputs)

        results = []

        for batch in range(0, len(inputs), batch_size):
            input_bach = inputs[batch:batch + batch_size]

            results_batch = asyncio.run(run_simulations(input_bach, self.url))

            results.extend(results_batch)

        self.save_run_outputs(results)

        return results

    def rerun_missing(self, input_dir: str = None, output_dir: str = None):
        input_dir = input_dir or os.path.join(self.work_dir, "inputs")
        output_dir = output_dir or os.path.join(self.work_dir, "outputs")

        if not os.path.exists(input_dir):
            raise ValueError("Input directory not found.")
        if not os.path.exists(output_dir):
            raise ValueError("Output directory not found.")

        input_files = [input_json for input_json in os.listdir(input_dir) if input_json.endswith('.json')]
        missing_inputs = []

        for input_file in input_files:
            input_id = input_file.split("_")[-1]
            output_path = os.path.join(output_dir, f"output_{input_id}")
            if not os.path.exists(output_path):
                input_path = os.path.join(input_dir, input_file)
                with open(input_path) as f:
                    missing_inputs.append(json.load(f))

        results = asyncio.run(run_simulations(missing_inputs, self.url))

        self.save_run_outputs(results, output_dir)

    def save_run_inputs(self, inputs: list, save_dir: str = None):
        save_dir = save_dir or os.path.join(self.work_dir, "inputs")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for input in inputs:
            output_path = os.path.join(save_dir, f"input_{input['run_id']}.json")
            with open(output_path, "w+") as f:
                json.dump(input, f, indent=4)

    def save_run_outputs(self, results: list, save_dir: str = None):
        save_dir = save_dir or os.path.join(self.work_dir, "outputs")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for result in results:
            output_path = os.path.join(save_dir, f"output_{result['run_id']}.json")
            with open(output_path, "w+") as f:
                json.dump(result, f, indent=4)

    def create_campaign(self, name: str, input_columns: list[str], output_columns: list[str],
                        inputs_dir: str = None, outputs_dir: str = None):
        if not os.path.exists(self.work_dir):  # used when importing external runs into campaign
            os.makedirs(self.work_dir)

        campaign = uq.Campaign(name=name + "_", work_dir=self.work_dir)
        campaign.add_app(name=name, params=self.params)
        campaign.set_sampler(self.sampler)

        inputs_dir = inputs_dir or os.path.join(self.work_dir, "inputs")
        outputs_dir = outputs_dir or os.path.join(self.work_dir, "outputs")
        input_files = absolute_filepaths(inputs_dir)
        output_files = absolute_filepaths(outputs_dir)

        if not output_files:
            raise ValueError("Output files not found")
        if len(output_files) < len(input_files):
            raise ValueError("Missing outputs, try running 'rerun_missing' method before.")

        input_decoder = uq.decoders.JSONDecoder(target_filename='_', output_columns=input_columns)
        output_decoder = uq.decoders.JSONDecoder(target_filename='_', output_columns=output_columns)

        campaign.add_external_runs(input_files, output_files, input_decoder, output_decoder)

        return campaign
