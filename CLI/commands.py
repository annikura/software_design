import os
import subprocess
from enum import Enum

import collectors
import mappers
import reducers
import validators


class CommandExecutor:
    @staticmethod
    def execute(command_str, args, piped):
        """
            Given a command, a list of its arguments and the piped data will
            run an appropriate command with the given parameters.

            :returns list of strings representing result of the command execution
        """
        pass


class CommandExecutorFromLine(CommandExecutor):
    @staticmethod
    def execute(command_str, args, piped):
        try:
            bs = subprocess.check_output(
                "echo \"{}\" | {} {}".format("" if piped is None else "\\n".join(piped), command_str, " ".join(args)),
                shell=True, stderr=open(os.devnull, 'wb'))
            return [bs.decode("utf-8")]
        except subprocess.CalledProcessError or subprocess.SubprocessError:
            raise CommandExecutionException("Error executing {}".format(command_str))


class MetaclassGeneratedCommandExecutor(CommandExecutor):
    commands = {}

    @staticmethod
    def execute(command_str, args, piped):
        command = MetaclassGeneratedCommandExecutor.commands.get(command_str)
        if command is None:
            raise CommandNotFoundException("Command {} was not found".format(command))
        else:
            return command().execute(*args, piped=piped)


class CommandExecutorMixedImpl(CommandExecutor):
    @staticmethod
    def execute(command_str, args, piped=None):
        try:
            return MetaclassGeneratedCommandExecutor.execute(command_str, args, piped)
        except CommandNotFoundException:
            return CommandExecutorFromLine.execute(command_str, args, piped)


class CommandExecutionException(Exception):
    pass


class CommandNotFoundException(Exception):
    pass


"""
    Every command is constructed with the use of the metaclass.
    It's been supposed that the command execution will often process through the following trivial steps:
    Input:  list of strings aka args
            list of strings aka piped data from the previous command
    
        * Validation of the arguments
        * Arguments mapping (i.e. "wc" would map its arguments to files content, so will do "cat")
        * Arguments reduce (we can concat or filter some data received from mapping)
        * Command evaluation on the result of the reduce
        * Collection of the results into the list of strings
    
    Output: list of strings as a result of the execution (multiple strings represent lines separated with "\n")
    
    So instead of implementing these parts completion multiple times it's been suggested to leave
    the command classes only with pure execution code and "config" which would describe which
    validator/reducer/... command is using. The rest part will be generated by metaclass.
    
    This will allow to perform most of the changes by changing metaclass only.
"""


class Metaclass(type):
    def __new__(mcs, class_name: str, class_parents, class_attributes: dict):
        validator = ValidatorEnum[class_attributes.get("validator", "NO")].get_validator()
        mapper = MapperEnum[class_attributes.get("mapper", "ID")].get_mapper()
        reducer = ReducerEnum[class_attributes.get("reducer", "ID")].get_reducer()
        collector = CollectorEnum[class_attributes.get("collector", "ID")].get_collector()

        def execute(cls, *args, piped=None):
            validation_result, validator_message = validator.validate(args, piped=piped)
            if not validation_result:
                raise InvalidCommandArgumentsException("{}: {}".format(class_name, validator_message))
            mapped_input = list(map(mapper.apply, list(args)))
            reduced_input = reducer.reduce(piped, mapped_input)
            return collector.collect(list([cls.__exec__(inp) for inp in reduced_input]))

        class_attributes["execute"] = execute

        clazz = type(class_name, class_parents, class_attributes)
        MetaclassGeneratedCommandExecutor.commands[class_attributes["command"]] = clazz
        return clazz


class InvalidCommandArgumentsException(Exception):
    pass


class ValidatorEnum(Enum):
    NO = validators.AlwaysTrue
    REQUIRE_ANY_INPUT = validators.RequiresAny
    REQUIRE_ARGS_INPUT = validators.RequiresArgs

    def __init__(self, validator):
        self.validator = validator

    def get_validator(self):
        return self.validator


class MapperEnum(Enum):
    ID = mappers.Id
    NAME_TO_FILE = mappers.NameToFile

    def __init__(self, mapper):
        self.mapper = mapper

    def get_mapper(self):
        return self.mapper


class ReducerEnum(Enum):
    ID = reducers.Id
    IGNORE_PIPED_AND_UNITE = reducers.IgnoresPipedAndUnites
    IGNORE_PIPED_IF_ARGS = reducers.IgnoresPipedIfArgs
    CALL_ONCE = reducers.CallOnce

    def __init__(self, reducer):
        self.reducer = reducer

    def get_reducer(self):
        return self.reducer


class CollectorEnum(Enum):
    ID = collectors.Id
    CONCAT_LISTS = collectors.ConcatLists

    def __init__(self, collector):
        self.collector = collector

    def get_collector(self):
        return self.collector


class Command:
    validator = "NO"
    mapper = "ID"
    reducer = "ID"
    collector = "ID"

    def execute(self, *args, piped=None):
        pass


class Wc(Command, metaclass=Metaclass):
    command = "wc"
    validator = "REQUIRE_ANY_INPUT"
    mapper = "NAME_TO_FILE"
    reducer = "IGNORE_PIPED_IF_ARGS"

    @classmethod
    def __exec__(cls, arg):
        return "{} {} {}".format(
            len(arg),
            sum(map(lambda x: len(x.split()), arg)),
            sum(map(len, arg))
        )


class Echo(Command, metaclass=Metaclass):
    command = "echo"
    reducer = "IGNORE_PIPED_AND_UNITE"

    @classmethod
    def __exec__(cls, arg):
        return " ".join(arg)


class Cat(Command, metaclass=Metaclass):
    command = "cat"
    mapper = "NAME_TO_FILE"
    reducer = "IGNORE_PIPED_IF_ARGS"
    collector = "CONCAT_LISTS"

    @classmethod
    def __exec__(cls, arg):
        return arg


class Exit(Command, metaclass=Metaclass):
    command = "exit"
    reducer = "CALL_ONCE"

    @classmethod
    def __exec__(cls, _):
        return exit()


class Pwd(Command, metaclass=Metaclass):
    command = "pwd"

    @classmethod
    def __exec__(cls, _):
        return os.path.dirname(os.path.realpath(__file__))
