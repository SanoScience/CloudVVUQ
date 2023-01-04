import unittest
from utils import *


class TestUtils(unittest.TestCase):
    def test_get_relative_filepaths(self):
        input_dir = "test_data/absolute_filepaths_data/inputs"
        input_filepaths = get_relative_filepaths(input_dir)

        expected = [
            Path("test_data", "absolute_filepaths_data", "inputs", "input_0.json"),
            Path("test_data", "absolute_filepaths_data", "inputs", "input_1.json"),
            Path("test_data", "absolute_filepaths_data", "inputs", "input_2.json"),
            Path("test_data", "absolute_filepaths_data", "inputs", "input_3.json"),
            Path("test_data", "absolute_filepaths_data", "inputs", "input_4.json"),
            Path("test_data", "absolute_filepaths_data", "inputs", "input_5.json")
        ]

        assert input_filepaths == expected


if __name__ == "__main__":
    unittest.main()
