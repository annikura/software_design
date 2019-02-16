from commands import CommandExecutorMixedImpl
from tokenizer import ParserContext, CommandLineParser, InvalidCommandException

if __name__ == "__main__":
    context = ParserContext()
    while True:
        print(">", end='')
        line = input()
        try:
            commands = CommandLineParser.parse_string(line, context)
            result = []
            for command in commands:
                result = CommandExecutorMixedImpl.execute(command[0], command[1:], piped=result)
            if result:
                print("\n".join(result))
        except InvalidCommandException as e:
            print(e.__cause__)
            continue
