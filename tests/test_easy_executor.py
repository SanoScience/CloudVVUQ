import os
import json
import unittest

import easyvvuq as uq
import chaospy as cp

from cloudvvuq.easy_executor import EasyExecutor

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../credentials/credentials.json'
url = "https://europe-west1-sano-332607.cloudfunctions.net/TubeDeflection"


class TestExecutor(unittest.TestCase):
    def _round_floats(self, obj):
        if isinstance(obj, float):
            return round(obj, 12)
        if isinstance(obj, dict):
            return {k: self._round_floats(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [self._round_floats(x) for x in obj]
        return obj

    params = {
        "F": {"type": "float", "default": 1.0},
        "L": {"type": "float", "default": 1.5},
        "a": {"type": "float", "min": 0.7, "max": 1.2, "default": 1.0},
        "D": {"type": "float", "min": 0.75, "max": 0.85, "default": 0.8},
        "d": {"type": "float", "default": 0.1},
        "E": {"type": "float", "default": 200000}
    }
    vary = {
        "F": cp.Normal(1, 0.1),
        "L": cp.Normal(1.5, 0.01),
        "a": cp.Uniform(0.7, 1.2),
        "D": cp.Triangle(0.75, 0.8, 0.85),
    }

    def test_draw_samples(self):
        sampler = uq.sampling.SCSampler(vary=self.vary, polynomial_order=3)

        executor = EasyExecutor("")
        executor.set_sampler(sampler, self.params)

        inputs = executor.draw_samples()

        with open("test_data/samples_data.json") as f:
            expected = json.load(f)

        assert self._round_floats(inputs) == self._round_floats(expected)

    def test_draw_samples_raises_for_infinite_generator(self):
        sampler = uq.sampling.RandomSampler(vary=self.vary)

        executor = EasyExecutor("")
        executor.set_sampler(sampler, self.params)

        with self.assertRaises(RuntimeError):
            executor.draw_samples()

    def test_draw_samples_raises_for_missing_default(self):
        bad_params = {
            "F": {"type": "float", "default": 1.0},
            "L": {"type": "float", "default": 1.5},
            "a": {"type": "float", "min": 0.7, "max": 1.2, "default": 1.0},
            "D": {"type": "float", "min": 0.75, "max": 0.85, "default": 0.8},
            "d": {"type": "float"},
        }
        sampler = uq.sampling.SCSampler(vary=self.vary, polynomial_order=3)

        executor = EasyExecutor("", "")
        executor.set_sampler(sampler, bad_params)

        with self.assertRaises(ValueError):
            executor.draw_samples()

    def test__prepare_samples(self):
        sampler = uq.sampling.SCSampler(vary=self.vary, polynomial_order=3)

        executor = EasyExecutor("")
        executor.set_sampler(sampler, self.params)

        inputs = executor.draw_samples()
        inputs = executor._prepare_samples(inputs)

        with open("test_data/prepared_samples_data.json") as f:
            expected = json.load(f)

        assert self._round_floats(inputs) == self._round_floats(expected)

    def test_run(self):
        sampler = uq.sampling.SCSampler(vary=self.vary, polynomial_order=3)

        executor = EasyExecutor(url)
        executor.set_sampler(sampler, self.params)

        inputs = executor.draw_samples(20)
        print(inputs)
        results = executor.run(inputs, cloud_provider="gcp")

        with open("test_data/results_20.json") as f:
            expected = json.load(f)

        assert self._round_floats(results) == self._round_floats(expected)

    def test_create_campaign(self):
        sampler = uq.sampling.SCSampler(vary=self.vary, polynomial_order=3)

        executor = EasyExecutor("", "")
        executor.set_sampler(sampler, self.params)

        campaign = executor.create_campaign(name="test_campaign",
                                            input_columns=['F', 'L', 'a', 'D', 'd', 'E'],
                                            output_columns=['g1', 'g2', 'g3'],
                                            inputs_dir="test_data/create_campaign_data/inputs",
                                            outputs_dir="test_data/create_campaign_data/outputs")

        campaign.apply_analysis(
            uq.analysis.SCAnalysis(
                sampler=campaign.get_active_sampler(),
                qoi_cols=["g1", 'g2', 'g3']
            )
        )

    def test_create_campaign_Value_Error(self):
        sampler = uq.sampling.SCSampler(vary=self.vary, polynomial_order=3)

        executor = EasyExecutor("")
        executor.set_sampler(sampler, self.params)

        with self.assertRaises(FileNotFoundError):
            campaign = executor.create_campaign(name="test_campaign",
                                                input_columns=['F', 'L', 'a', 'D', 'd', 'E'],
                                                output_columns=['g1', 'g2', 'g3'],
                                                inputs_dir="test_data/create_campaign_data/inputs",
                                                outputs_dir="test_data/create_campaign_data/fake_dir_outputs")

    def test__find_n_samples(self):
        executor = EasyExecutor(url)

        executor.set_sampler(uq.sampling.SCSampler(vary=self.vary, polynomial_order=4), self.params)
        assert executor._find_max_samples(800) == 625
        assert executor._find_max_samples(100) == 100
        assert executor._find_max_samples(0) == 625

        executor.set_sampler(uq.sampling.PCESampler(vary=self.vary), self.params)
        assert executor._find_max_samples(800) == 625
        assert executor._find_max_samples(100) == 100
        assert executor._find_max_samples(0) == 625

        executor.set_sampler(uq.sampling.RandomSampler(vary=self.vary), self.params)
        assert executor._find_max_samples(800) == 800
        assert executor._find_max_samples(100) == 100
        assert executor._find_max_samples(0) == 0

        executor.set_sampler(uq.sampling.CSVSampler("test_data/samples.csv"), self.params)
        assert executor._find_max_samples(800) == 625
        assert executor._find_max_samples(100) == 100
        assert executor._find_max_samples(0) == 625

        executor.set_sampler(uq.sampling.QMCSampler(vary=self.vary, n_mc_samples=5), self.params)
        assert executor._find_max_samples(800) == 30
        assert executor._find_max_samples(20) == 20
        assert executor._find_max_samples(0) == 30


if __name__ == "__main__":
    unittest.main()
