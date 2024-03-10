import logging
import os
import shutil
import unittest

from dotenv import load_dotenv
from slack_ai.utils.flatten_files import flatten_files, get_logger
from slack_ai.utils.html2markdown_file import html2markdown_dir

load_dotenv()

DATA_SOURCE_FOLDER = os.environ['DATA_SOURCE_FOLDER']
DATA_TARGET_FOLDER = os.environ['DATA_TARGET_FOLDER']
TMP_FOLDER = os.environ['TMP_FOLDER']

## A12 asciidocs
# Flatten files from raw source to temp target
tmp_asciidoc = os.path.join(TMP_FOLDER, "A12_asciidoc_flat")
flatten_files(os.path.join(DATA_SOURCE_FOLDER, "A12/A12_asciidoc_2022.06"), tmp_asciidoc, pattern='*.html')

# Transform the html to maerkdown
html2markdown_dir(tmp_asciidoc, DATA_TARGET_FOLDER)