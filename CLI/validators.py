"""
        Validators are classes that contain "validate" method and check command arguments on validity.
"""


class Validator:
    @staticmethod
    def validate(*args, piped):
        pass


class AlwaysTrue(Validator):
    @staticmethod
    def validate(*args, piped):
        return True, ""


class RequiresAny(Validator):
    @staticmethod
    def validate(*args, piped):
        result = args or piped
        message = ""
        if not result:
            message = "invalid arguments: command requires either args or piped to be present"
        return result, message


class RequiresArgs(Validator):
    @staticmethod
    def validate(*args, piped):
        result = len(args) > 0
        message = ""
        if not result:
            message = "invalid arguments: command requires args to be present"
        return result, message
