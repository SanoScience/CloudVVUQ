import os
import json
import unittest
from pathlib import Path

from cloudvvuq.executor import Executor

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

    def test_run(self):
        executor = Executor(url)
        inputs = [{'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.0349952608962139, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.762453742834778, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.7868885078673565, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.8131114921326246, 'd': 0.1, 'E': 200000}, {'F': 0.7665585781661023, 'L': 1.4925803621569729, 'a': 0.7347159221014868, 'D': 0.837546257165213, 'd': 0.1, 'E': 200000}]
        results = executor.run(inputs, cloud_provider="gcp")

        with open("test_data/results_20.json") as f:
            expected = json.load(f)

        assert self._round_floats(results) == self._round_floats(expected)

    def test_find_inputs_to_rerun(self):
        run_dir = Path(Path(__file__).parent, "test_data", "rerun_missing_simulations_data")
        executor = Executor(url, run_dir)

        outputs_to_remove = ["output_0.json", "output_5.json", "output_15.json", "output_40.json", "output_49.json"]
        output_filepaths = [Path(run_dir, "outputs", output_file) for output_file in outputs_to_remove]
        for output_filepath in output_filepaths:
            if output_filepath.exists():
                Path.unlink(output_filepath)

        missing_inputs = executor.find_inputs_to_rerun()

        expected = [{'D': 0.762453742834778, 'E': 200000, 'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.7347159221014868, 'd': 0.1, 'input_id': 0, 'sim_gcs_path': 'inputs/beam'}, {'D': 0.837546257165213, 'E': 200000, 'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 1.1652840778985132, 'd': 0.1, 'input_id': 15, 'sim_gcs_path': 'inputs/beam'}, {'D': 0.762453742834778, 'E': 200000, 'F': 0.7665585781661023, 'L': 1.5074196378430273, 'a': 1.0349952608962139, 'd': 0.1, 'input_id': 40, 'sim_gcs_path': 'inputs/beam'}, {'D': 0.7868885078673565, 'E': 200000, 'F': 0.7665585781661023, 'L': 1.52334414218339, 'a': 0.7347159221014868, 'd': 0.1, 'input_id': 49, 'sim_gcs_path': 'inputs/beam'}, {'D': 0.7868885078673565, 'E': 200000, 'F': 0.7665585781661023, 'L': 1.4766558578166098, 'a': 0.8650047391037858, 'd': 0.1, 'input_id': 5, 'sim_gcs_path': 'inputs/beam'}]

        assert missing_inputs == expected


if __name__ == "__main__":
    unittest.main()
