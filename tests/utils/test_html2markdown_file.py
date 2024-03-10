import unittest
import os
from slack_ai.utils.html2markdown_file import html2markdown_file, html2markdown_dir


class TestHtml2Markdown(unittest.TestCase):
    def setUp(self):
        self.TEST_DIR = "data/test/html2markdown_files"
        os.makedirs(self.TEST_DIR, exist_ok=True)
        self.html_content = "<h1>Hello, World!</h1>"
        self.markdown_content = "# Hello, World!\n\n"
        self.html_file_path = os.path.join(self.TEST_DIR, "test.html")
        self.markdown_file_path = os.path.join(self.TEST_DIR, "test.md")
        with open(self.html_file_path, 'w') as f:
            f.write(self.html_content)

    def test_html2markdown_file(self):
        html2markdown_file(self.html_file_path, self.markdown_file_path)
        with open(self.markdown_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.markdown_content)

    def test_html2markdown_dir(self):
        html2markdown_dir(self.TEST_DIR, self.TEST_DIR)
        with open(self.markdown_file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.markdown_content)

    def test_html2markdown_dir_with_empty_source_dir(self):
        if os.path.exists(self.html_file_path):
            os.remove(self.html_file_path)
        html2markdown_dir(self.TEST_DIR, self.TEST_DIR)
        
        
    def tearDown(self):
        if os.path.exists(self.html_file_path):
            os.remove(self.html_file_path)
        if os.path.exists(self.markdown_file_path):
            os.remove(self.markdown_file_path)

if __name__ == '__main__':
    unittest.main()
