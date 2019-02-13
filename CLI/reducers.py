"""
    Reducers are classes that contain "reduce" method and reduce results from mapper to command input.
"""
import mappers


class Reducer:
    @staticmethod
    def reduce(piped, args):
        pass


class Id(Reducer):
    @staticmethod
    def reduce(piped, args):
        """
        Concatenates piped argument with args into the list.

        :param piped: piped argument
        :param args: command arguments
        :return: list with all provided arguments
        """
        return [piped] + args


class IgnoresPipedAndUnites(Reducer):
    @staticmethod
    def reduce(piped, args):
        """
        Ignores piped argument and returns args wrapped into a list.

        :param piped: piped argument
        :param args: command arguments
        :return: args unchanged
        """
        return [args]


class IgnoresPipedIfArgs(Reducer):
    @staticmethod
    def reduce(piped, args):
        """
        Ignores piped argument if args were provided.

        :param piped: piped argument
        :param args: command arguments
        :return: result arguments
        """
        if args:
            return args
        else:
            return [piped]


class CallOnce(Reducer):
    @staticmethod
    def reduce(_, __):
        """
        Ignores all provided input and returns [[]] in order to make a command to be called once an an empty input.

        :return: [[]]
        """
        return [[]]


class SecondToFileOrPiped(Reducer):
    @staticmethod
    def reduce(piped, args):
        """
        Takes two first arguments from args, if they exist and maps the second one to file.
        In case if len(args) == 1, will take piped as a file content.
        Expects that at least two parameters in sum with piped will be provided.

        :param piped: piped argument
        :param args: command arguments
        :return: list of two elements: first argument and list of string representing data
        """
        return [[args[0], piped if len(args) == 1 else mappers.NameToFile.apply(args[1])]]
