import shutil
import tempfile
import unittest
from os import path

import commands


class TestCommands(unittest.TestCase):
    def create_tmp_file(self, filename, file_content):
        file_path = path.join(self.test_dir, filename)
        with open(file_path, 'w') as file:
            file.writelines('\n'.join(file_content))
        return file_path

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_wc_exec(self):
        self.assertEqual("2 3 12", commands.Wc.__exec__(["some word", "hey"]))

    def test_wc_execute_from_pipe(self):
        self.assertEqual(["1 2 9"], commands.Wc().execute(piped=["some word"]))

    def test_wc_execute_from_pipe_with_multiple_lines(self):
        self.assertEqual(["2 2 2"], commands.Wc().execute(piped=["a", "b"]))

    def test_wc_execute_from_args(self):
        self.assertEqual(["2 3 13"], commands.Wc().execute(
            self.create_tmp_file("test_file", ["some test", "here"])))

    def test_wc_execute_ignores_piped_when_has_args(self):
        self.assertEqual(["1 3 13"], commands.Wc().execute(
            self.create_tmp_file("test_file1", ["just one line"]), piped=["One more"]))

    def test_echo_ignores_piped(self):
        self.assertEqual([''], commands.Echo().execute(piped=["something"]))

    def test_echo_word(self):
        self.assertEqual(["word"], commands.Echo().execute("word", piped=["something"]))

    def test_echo_several_word(self):
        self.assertEqual(["word another with   spaces"], commands.Echo().execute("word", "another", "with   spaces"))

    def test_cat_from_piped(self):
        self.assertEqual(["something"], commands.Cat().execute(piped=["something"]))

    def test_cat_from_piped_with_multiple_lines(self):
        self.assertEqual(["something", "another somthing"], commands.Cat()
                         .execute(piped=["something", "another somthing"]))

    def test_cat_from_one_file(self):
        self.assertEqual(["some test", "here"], commands.Cat().execute(
            self.create_tmp_file("test_file", ["some test", "here"])))

    def test_cat_from_two_files(self):
        self.assertEqual(["some text", "here", "another text", "there"], commands.Cat().execute(
            self.create_tmp_file("test_file1", ["some text", "here"]),
            self.create_tmp_file("test_file2", ["another text", "there"])))

    def test_cat_ignores_piped_when_args_present(self):
        self.assertEqual(["some test", "here"], commands.Cat().execute(
            self.create_tmp_file("test_file", ["some test", "here"]), piped=["piped"]))
