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
        self.assertEqual("2 3 12\n", commands.Wc.__exec__(["some word", "hey"]))

    def test_wc_execute_from_pipe(self):
        self.assertEqual(["1 2 9\n"], commands.Wc().execute(piped=["some word"]))

    def test_wc_execute_from_pipe_with_multiple_lines(self):
        self.assertEqual(["2 2 2\n"], commands.Wc().execute(piped=["a", "b"]))

    def test_wc_execute_from_args(self):
        self.assertEqual(["2 3 14\n"], commands.Wc().execute(
            self.create_tmp_file("test_file", ["some test", "here"])))

    def test_wc_execute_ignores_piped_when_has_args(self):
        self.assertEqual(["1 3 13\n"], commands.Wc().execute(
            self.create_tmp_file("test_file1", ["just one line"]), piped=["One more"]))

    def test_echo_ignores_piped(self):
        self.assertEqual(['\n'], commands.Echo().execute(piped=["something"]))

    def test_echo_word(self):
        self.assertEqual(["word\n"], commands.Echo().execute("word", piped=["something"]))

    def test_echo_several_word(self):
        self.assertEqual(["word another with   spaces\n"], commands.Echo().execute("word", "another", "with   spaces"))

    def test_cat_from_piped(self):
        self.assertEqual(["something\n"], commands.Cat().execute(piped=["something"]))

    def test_cat_from_piped_with_multiple_lines(self):
        self.assertEqual(["something\n", "another somthing\n"], commands.Cat()
                         .execute(piped=["something\n", "another somthing"]))

    def test_cat_from_one_file(self):
        self.assertEqual(["some test\n", "here\n"], commands.Cat().execute(
            self.create_tmp_file("test_file", ["some test", "here"])))

    def test_cat_from_two_files(self):
        self.assertEqual(["some text\n", "here\n", "another text\n", "there\n"], commands.Cat().execute(
            self.create_tmp_file("test_file1", ["some text", "here"]),
            self.create_tmp_file("test_file2", ["another text", "there"])))

    def test_cat_ignores_piped_when_args_present(self):
        self.assertEqual([" some test \n", "here\n"], commands.Cat().execute(
            self.create_tmp_file("test_file", [" some test ", "here"]), piped=["piped"]))

    def test_simple_grep_from_pipe(self):
        self.assertEqual(["this is test"], commands.Grep().execute("hi", piped=["this is test"]))

    def test_simple_grep_from_file(self):
        self.assertEqual(["some hi-test\n"], commands.Grep().execute(
            "hi", self.create_tmp_file("test_file", ["some hi-test", "here"])))

    def test_grep_regexp(self):
        self.assertEqual(["this is test", "maysbe yes"],
                         commands.Grep().execute("s*s",
                                                 piped=["this is test", "or quite hot", "maysbe yes", "maybe not"]))

    def test_grep_w_flag(self):
        self.assertEqual(["this is test"],
                         commands.Grep().execute("-w", "t..t",
                                                 piped=["this is test", "tester is testing"]))

    def test_grep_i_flag(self):
        self.assertEqual(["this is Test!", "TESTING"],
                         commands.Grep().execute("-i", "t..t",
                                                 piped=["this is Test!", "TESTING"]))

    def test_grep_A_flag(self):
        self.assertEqual(["this is test", "a", "testing"],
                         commands.Grep().execute("-A", "1", "t..t",
                                                 piped=["this is test", "a", "b", "c", "testing"]))

    def test_grep_A_overlap_flag(self):
        self.assertEqual(["this is test", "testing", "a", "b"],
                         commands.Grep().execute("-A", "2", "t..t",
                                                 piped=["this is test", "testing", "a", "b", "c"]))

    def test_grep_validator(self):
        self.assertRaises(commands.InvalidCommandArgumentsException, lambda: commands.Grep().execute("f", "-A", "2"))
