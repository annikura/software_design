import re
import subprocess
from enum import Enum, auto


class Mode(Enum):
    NORMAL = auto()
    WEAK_QUOTES = auto(),
    FULL_QUOTES = auto()


class InvalidContextReferenceException(Exception):
    pass


"""
    A context class containing environmental and custom variables.
"""


class ParserContext:
    def __init__(self):
        self.values = {}

    def get_variable(self, variable):
        """
        Attempts to get the variable from the custom set. In case of failure, gets the variable from the system ENV.

        :param variable: name of the variable to be retrieved
        :return: value stored by variable
        """
        value = self.values.get(variable)
        if value is None:
            try:
                bs = subprocess.check_output(
                    "echo ${}".format(variable),
                    shell=True)
                return bs.decode("utf-8").strip()
            except subprocess.CalledProcessError:
                raise InvalidContextReferenceException("Unknown variable: {}".format(variable))
        return value

    def set_variable(self, variable, value):
        self.values[variable] = value

    def contains_variable(self, variable):
        return variable in self.values


class InvalidCommandException(Exception):
    pass


"""
    Given a string, CommandLineParser will detect weather it's a command execution or an assignment
    and depending on that will either perform assignment of the variable into the context or will
    split line into consequent lists storing commands and their arguments replacing all the known variables on its way. 
"""


class CommandLineParser:
    special_symbols = {
        Mode.NORMAL: "\"'$\\| ",
        Mode.WEAK_QUOTES: "\"$\\",
        Mode.FULL_QUOTES: "'\\"
    }

    @staticmethod
    def __switch_modes(current_mode, mode_a, mode_b):
        if current_mode is mode_a:
            return mode_b
        if current_mode is mode_b:
            return mode_a
        return current_mode

    @staticmethod
    def __refresh_token(new_token, tokens):
        if new_token:
            tokens.append(new_token)
        return ""

    @staticmethod
    def __get_variable_name_as_prefix(s: str):
        if not s or not (s[0].isalpha() or s[0] == '_'):
            # no character to begin with
            return -1, None
        for i in range(len(s)):
            sym = s[i]
            if sym.isalnum() or sym == '_':
                continue
            else:
                return i, s[:i]
        return len(s), s

    @staticmethod
    def __group_tokens_into_commands(tokens):
        if not tokens:
            return []

        commands = []
        command = []
        for token in tokens:
            if token == "|":
                if not command:
                    raise InvalidCommandException("Pipes locations create an empty command.")
                commands.append(command)
                command = []
            else:
                command.append(token)
        if not command:
            raise InvalidCommandException("Pipes locations create an empty command.")
        commands.append(command)
        return commands

    @staticmethod
    def parse_string(s: str, context: ParserContext):
        """
        Given a string containing a sequence of commands and env variables makes env variables substitutions,
        removes wrapping quotes and parses a line into sequential lists each containing a command and its arguments.

        :param s: command string
        :param context: environment context
        :return: list of commands to be executed.

        NOTICE: an assignment operation will always execute itself and return an empty list.
        """
        if re.match("^\\s*\\w[\\w0-9_]*\\s*=.*$", s):
            CommandLineParser.parse_assignment(s, context)
            return []
        else:
            return CommandLineParser.__group_tokens_into_commands(CommandLineParser.parse_command_line(s, context))

    @staticmethod
    def parse_assignment(s: str, context):
        """
        Given a string containing an assignment operation, performs assignment operation on a given context.

        :param s: string with assignment.
        :param context: environment context
        :return: a tuple of a variable name, its new value set by the command and
        its old value or None if it didn't exist before
        """
        eq_index = s.find('=')
        variable = s[:eq_index].strip()
        value = ""
        rest_tokens = CommandLineParser.parse_command_line(s[eq_index + 1:], context)
        if rest_tokens:
            value = rest_tokens[0]
            if len(rest_tokens) > 1:
                raise InvalidCommandException(
                    "Too many values for variable assignment: {}".format(", ".join(rest_tokens)))
        old_value = None if not context.contains_variable(variable) else context.get_variable(variable)
        context.set_variable(variable, value)
        return variable, value, old_value

    @staticmethod
    def parse_command_line(s: str, context: ParserContext):
        """
        Given a line containing sequential commands, parses it into a list of lists each
        containing a command and its arguments.

        :param s: line to be parsed
        :param context: env context
        :return: list of commands
        """
        mode = Mode.NORMAL
        tokens = []
        last_token = ""
        is_escaped = False
        next_int = 0

        for i in range(len(s)):
            if i < next_int:
                continue

            sym = s[i]

            if is_escaped:
                is_escaped = False
                last_token += sym
                continue
            if sym not in CommandLineParser.special_symbols[mode]:
                last_token += sym
                continue
            # sym is a special symbol
            if sym is '\\':
                is_escaped = True
                continue
            if sym is ' ':
                last_token = CommandLineParser.__refresh_token(last_token, tokens)
                continue
            if sym is '\'':
                mode = CommandLineParser.__switch_modes(mode, Mode.FULL_QUOTES, Mode.NORMAL)
                continue
            if sym is '"':
                mode = CommandLineParser.__switch_modes(mode, Mode.WEAK_QUOTES, Mode.NORMAL)
                continue
            if sym is '|':
                last_token = CommandLineParser.__refresh_token(last_token, tokens)
                tokens.append("|")
                continue
            if sym is "$":
                length, name = CommandLineParser.__get_variable_name_as_prefix(s[i + 1:])
                last_token += context.get_variable(name)
                next_int = i + length + 1

        if mode is not Mode.NORMAL:
            raise InvalidCommandException("Quotes mismatch")

        CommandLineParser.__refresh_token(last_token, tokens)
        return tokens
