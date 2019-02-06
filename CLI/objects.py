import re


class Command:
    @staticmethod
    def exec(command, *args, piped=None):
        {
            "wc": Command.wc
        }[command](args, piped)

    @staticmethod
    def wc(*args, piped=None):
        def get_text_stats(text):
            return "{} {} {}".format(
                len(text),
                sum(map(lambda x: len(re.findall(r'[^\s]+', x)), text)),
                sum(map(len, text)))

        def get_file_stats(filename: str):
            try:
                with open(filename) as file:
                    return get_text_stats(file.readlines())
            except IOError as e:
                raise CliException("Error: " + str(e))

        return [get_text_stats(piped)] + list(map(get_file_stats, args))

    @staticmethod
    def echo(*args, piped=None):
        result = []
        if piped is not None:
            result.append(piped)
        for arg in args:
            result += arg.exec()


class CliException(Exception):
    pass
