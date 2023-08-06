
from script import ls, cat, grep

def repl():
    state = '.'  # Initial state is the current directory

    while True:
        # Read user input
        command_line = input('> ')
        command, *args = command_line.split()

        # Parse and execute the command
        if command == 'ls':
            result, state = ls(*args).run(state)
            print(result)
        elif command == 'cat':
            result, state = cat(*args).run(state)
            print(result)
        elif command == 'grep':
            pattern, filename = args
            result, state = cat(filename).bind(lambda text: grep(pattern, text)).run(state)
            print(result)
        elif command == 'exit':
            break
        else:
            print(f'Unknown command: {command}')

if __name__ == "__main__":
    repl()
