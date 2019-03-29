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
