"""
    Mapper are classes that contain "apply" method and map command argument into some other value.
"""


class Mapper:
    @staticmethod
    def apply(arg):
        pass


class Id(Mapper):
    @staticmethod
    def apply(arg):
        """
        Identity mapper executor. Returns given parameter unchanged
        """
        return arg


class NameToFile(Mapper):
    @staticmethod
    def apply(filename):
        """
        Given a name of file returns its content as a list of string
        :param filename: name of the file to be read
        :return: file content
        """
        with open(filename) as file:
            return file.readlines()


class NameToFileAndName(Mapper):
    @staticmethod
    def apply(filename):
        """
        Given a name of file returns a pair of its name and its content as a list of string
        :param filename: name of the file to be read
        :return: (name, file content)
        """
        with open(filename) as file:
            return filename, file.readlines()
