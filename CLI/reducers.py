"""
    Reducers are classes that contain "reduce" method and reduce results from mapper to command input.
"""


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

        :param piped: piped argument
        :param args: command arguments
        :return: [[]]
        """
        return [[]]
