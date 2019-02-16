import unittest

from tokenizer import ParserContext, CommandLineParser, InvalidCommandException


class TestParsers(unittest.TestCase):
    def test_parse_assignment(self):
        context = ParserContext()
        CommandLineParser.parse_assignment("foo=bar", context)
        self.assertEqual("bar", context.get_variable("foo"))

    def test_parse_assignment_with_odd_spaces(self):
        context = ParserContext()
        CommandLineParser.parse_assignment("  a  = something  ", context)
        self.assertEqual("something", context.get_variable("a"))

    def test_parse_assignment_with_quotes(self):
        context = ParserContext()
        CommandLineParser.parse_assignment("foo='bar'k", context)
        self.assertEqual("bark", context.get_variable("foo"))

    def test_parse_assignment_with_too_many_values(self):
        context = ParserContext()
        self.assertRaises(InvalidCommandException, lambda: CommandLineParser.parse_assignment("foo=b k", context))

    def test_parse_command_line(self):
        context = ParserContext()
        tokens = CommandLineParser.parse_command_line("echo 'gav\\\''ga'v' dogg| cat", context)
        self.assertEqual(["echo", "gav'gav", "dogg", "|", "cat"], tokens)

    def test_parse_string(self):
        context = ParserContext()
        tokens = CommandLineParser.parse_string("echo 'gav\\\''ga'v' dogg| cat", context)
        self.assertEqual([["echo", "gav'gav", "dogg"], ["cat"]], tokens)

    def test_parse_invalid_command_line(self):
        context = ParserContext()
        self.assertRaises(InvalidCommandException,
                          lambda: CommandLineParser.parse_command_line("echo 'gav''ga'v' dogg| cat", context))

    def test_parse_invalid_command_line_string(self):
        context = ParserContext()
        self.assertRaises(InvalidCommandException,
                          lambda: CommandLineParser.parse_string("echo  dogg| cat |", context))

    def test_parse_command_line_with_variable(self):
        context = ParserContext()
        CommandLineParser.parse_string("a=boo", context)
        tokens = CommandLineParser.parse_command_line("echo $a 'ga v$a' \"d o$a|gg\"", context)
        self.assertEqual(["echo", "boo", "ga v$a", "d oboo|gg"], tokens)

    def test_parse_command_line_with_unknown_variable(self):
        context = ParserContext()
        tokens = CommandLineParser.parse_command_line("echo $a 'ga v$a' \"d o$a|gg\"", context)
        self.assertEqual(["echo", "ga v$a", "d o|gg"], tokens)
