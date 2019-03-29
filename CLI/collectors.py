"""
    Collectors are classes that contain "collect" method and reduce list of results from command to final result.
"""


class Collector:
    @staticmethod
    def collect(results):
        pass


class Id(Collector):
    @staticmethod
    def collect(results):
        """
        Trivial collector.
        :param results: it is expected that results will be a list of strings.
        :return: results variable.
        """
        return results


class ConcatLists(Collector):
    @staticmethod
    def collect(results):
        """
        Concatenates a list of lists of strings into a one big list.
        :param results: [[string]]
        :return: concatenated list
        """
        return sum(results, [])
