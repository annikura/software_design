import unittest

from tokenizer import Context, CommandLineParser, InvalidCommandException


class TestCommands(unittest.TestCase):
    def test_parse_assignment(self):
        context = Context()
        CommandLineParser.parse_assignment("foo=bar", context)
        self.assertEqual("bar", context.get_value("foo"))

    def test_parse_assignment_with_odd_spaces(self):
        context = Context()
        CommandLineParser.parse_assignment("  a  = something  ", context)
        self.assertEqual("something", context.get_value("a"))

    def test_parse_assignment_with_quotes(self):
        context = Context()
        CommandLineParser.parse_assignment("foo='bar'k", context)
        self.assertEqual("bark", context.get_value("foo"))

    def test_parse_assignment_with_too_many_values(self):
        context = Context()
        self.assertRaises(InvalidCommandException, lambda: CommandLineParser.parse_assignment("foo=b k", context))

    def test_parse_command_line(self):
        context = Context()
        tokens = CommandLineParser.parse_command_line("echo 'gav\\\''ga'v' dogg| cat", context)
        self.assertEqual(["echo", "gav'gav", "dogg", "|", "cat"], tokens)

    def test_parse_string(self):
        context = Context()
        tokens = CommandLineParser.parse_string("echo 'gav\\\''ga'v' dogg| cat", context)
        self.assertEqual([["echo", "gav'gav", "dogg"], ["cat"]], tokens)

    def test_parse_invalid_command_line(self):
        context = Context()
        self.assertRaises(InvalidCommandException,
                          lambda: CommandLineParser.parse_command_line("echo 'gav''ga'v' dogg| cat", context))

    def test_parse_invalid_command_line_string(self):
        context = Context()
        self.assertRaises(InvalidCommandException,
                          lambda: CommandLineParser.parse_string("echo  dogg| cat |", context))

    def test_parse_trash_string(self):
        context = Context()
        self.assertRaises(InvalidCommandException,
                          lambda: CommandLineParser.parse_string("sdjglkd635643@$UI#sgdlu9rers (*$*#3 4", context))

    def test_parse_command_line_with_variable(self):
        context = Context()
        CommandLineParser.parse_string("a=boo", context)
        tokens = CommandLineParser.parse_command_line("echo $a 'ga v$a' \"d o$a|gg\"", context)
        self.assertEqual(["echo", "boo", "ga v$a", "d oboo|gg"], tokens)

    def test_parse_command_line_with_unknown_variable(self):
        context = Context()
        self.assertRaises(InvalidCommandException,
                          lambda: CommandLineParser.parse_command_line("echo $a 'ga v$a' \"d o$a|gg\"", context))
