import logging
import os
import shutil
import unittest
from slack_ai.utils.flatten_files import flatten_files, get_logger

class TestFlattenFiles(unittest.TestCase):

    def setUp(self):
        # Clean the data/tmp/flatten_files directory before each test
        shutil.rmtree('data/tmp/flatten_files', ignore_errors=True)
        os.makedirs('data/tmp/flatten_files', exist_ok=True)

    def test_flatten_files(self):
        input_folder = 'data/test/flatten_files/A'
        output_folder = 'data/tmp/flatten_files/out'

        flatten_files(input_folder, output_folder)

        # Check if the output directory exists
        self.assertTrue(os.path.isdir(output_folder))

       # Check if the expected files exist in the output directory
        expected_files = ['A_B_a_b.json', 'A_C_a_c.txt']
        actual_files = os.listdir(output_folder)
        for file in expected_files:
            self.assertIn(file, actual_files)

    
if __name__ == '__main__':
    unittest.main()
