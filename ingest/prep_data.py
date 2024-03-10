import logging
import os
import shutil
import unittest

from dotenv import load_dotenv
from slack_ai.utils.flatten_files import flatten_files, get_logger

load_dotenv()

DATA_SOURCE_FOLDER = os.environ['DATA_SOURCE_FOLDER']
DATA_TARGET_FOLDER = os.environ['DATA_TARGET_FOLDER']

flatten_files(DATA_SOURCE_FOLDER, DATA_TARGET_FOLDER, pattern='*.html')
