from chalicelib import utils
import unittest
import pytest
import glob
import json


class EhbaUtilsTest(unittest.TestCase):
    def test_upload_empty(self):
        data = []
        data, results = utils.parsed_json_files_to_dataframe(data)
        self.assertEqual(results, {})
    
    def test_json_upload_single_files(self):
        for file in glob.glob("tests/data/*.json"):
            print("Testing: {}".format(file))
            data = json.loads(open(file, "r").read())
            files = data.get('files')
            self.assertEqual(len(files), 1)
            data, results = utils.parsed_json_files_to_dataframe(files)
            self.assertNotEqual(results, None)
            self.assertIn('years', results)

    def test_json_upload_multiple_files(self):
        files = []
        for file in glob.glob("tests/data/*.json"):
            data = json.loads(open(file, "r").read())
            files.append(data.get('files')[0])

        self.assertEqual(len(files), len(glob.glob("tests/data/*.json")))

        data, results = utils.parsed_json_files_to_dataframe(files)
        self.assertIn('years', results)

