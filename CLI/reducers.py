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
        return [piped] + args


class IgnoresPiped(Reducer):
    @staticmethod
    def reduce(piped, args):
        return [args]


class IgnoresPipedIfArgs(Reducer):
    @staticmethod
    def reduce(piped, args):
        if args:
            return args
        else:
            return [piped]


class CallOnce(Reducer):
    @staticmethod
    def reduce(_, __):
        return [[]]


class SecondToFileOrPiped(Reducer):
    @staticmethod
    def reduce(piped, args):
        return [[args[0], piped if len(args) == 1 else mappers.NameToFile.apply(args[1])]]
