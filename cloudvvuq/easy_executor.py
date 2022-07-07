from pathlib import Path

from tqdm import tqdm
import easyvvuq as uq

from executor import Executor
from utils import get_relative_filepaths


class EasyExecutor(Executor):
    sampler: uq.sampling
    params: dict

    def __init__(self, url: str, work_dir: [Path, str] = None):
        super().__init__(url, work_dir)

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
