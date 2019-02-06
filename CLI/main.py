from commands import CommandExecutor
from tokenizer import Context, CommandLineParser, InvalidCommandException

if __name__ == "__main__":
    context = Context()
    while True:
        print(">", end='')
        line = input()
        try:
            commands = CommandLineParser.parse_string(line, context)
            result = []
            for command in commands:
                result = CommandExecutor.execute(command[0], command[1:], piped=result)
            if result:
                print("\n".join(result))
        except InvalidCommandException as e:
            print(e.__cause__)
            continue
