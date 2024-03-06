import os
import shutil
import unittest
from slack_ai.utils.dict2file import write_dict_to_file, read_dict_from_file

FILENAME = "data/test/dict2file/test.json"

class TestDict2file(unittest.TestCase):

    def setUp(self):
        # Clean the data/tmp/flatten_files directory before each test
        shutil.rmtree('data/tmp/dict2file', ignore_errors=True)

    def test_write_dict_to_file(self):
        data = {
            "hello": "world",
            "now": "what"
        }
        write_dict_to_file(dictionary=data, full_filename=FILENAME)


    def test_read_dict_from_file(self):
        data = {
            "hello": "world",
            "now": "what"
        }

        # Write and then read it
        write_dict_to_file(dictionary=data, full_filename=FILENAME)
        data2 = read_dict_from_file(full_filename=FILENAME)

        # Delete test data, try to read it - even though it doesn't exist
        try:
            os.remove(FILENAME)
        except FileNotFoundError:
            pass
        try:
            data3 = read_dict_from_file(full_filename=FILENAME)
        except:
            print("All good, I am in an exception as I expected it to be")


if __name__ == '__main__':
    unittest.main()
