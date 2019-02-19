"""
    Validators are classes that contain "validate" method and check list of command arguments on validity.
"""


class Validator:
    @staticmethod
    def validate(*args, piped):
        """
        :return: true if input is valid, false if not.
        """
        pass


class AlwaysTrue(Validator):
    @staticmethod
    def validate(*args, piped):
        return True, ""


class RequiresAny(Validator):
    @staticmethod
    def validate(*args, piped):
        """
        Checks that either args or piped input was provided

        :param args: list of command arguments
        :param piped: text piped to command
        """
        result = args or piped
        message = ""
        if not result:
            message = "invalid arguments: command requires either args or piped to be present"
        return result, message


class RequiresArgs(Validator):
    @staticmethod
    def validate(*args, piped):
        """
        Checks that args were provided

        :param args: list of command arguments
        :param piped: text piped to command
        """
        result = len(args) > 0
        message = ""
        if not result:
            message = "invalid arguments: command requires args to be present"
        return result, message


class AtLeastTwoWithPiped(Validator):
    @staticmethod
    def validate(*args, piped):
        """
        Checks that at least two args including piped are provided

        :param args: list of command arguments
        :param piped: text piped to command
        """
        if ((piped is not None) + len(args)) >= 2:
            return True, ""
        else:
            return False, "invalid arguments: command requires two args: PATTERN, FILE"


class OneOrZeroArguments(Validator):
    @staticmethod
    def validate(*args, piped):
        """
        Checks that one or zero arguments are provided

        :param args: list of command arguments
        :param piped: text piped to command
        """
        if len(args) <= 1:
            return True, ""
        else:
            return False, "invalid arguments: expected one or zero arguments"
