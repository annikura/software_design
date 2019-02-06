"""
    Mapper are classes that contain "apply" method and map command arguments into some other values.
"""

class Mapper:
    @staticmethod
    def apply(arg):
        pass


class Id(Mapper):
    @staticmethod
    def apply(arg):
        return arg


class NameToFile(Mapper):
    @staticmethod
    def apply(filename):
        with open(filename) as file:
            return list(map(lambda x: x.rstrip(), file.readlines()))

