
from typing import Callable, Tuple, TypeVar, List
import os
import re

S = TypeVar('S')  # The type of the state
A = TypeVar('A')  # The type of the value

class State:
    def __init__(self, function: Callable[[S], Tuple[A, S]]):
        self.function = function

    def bind(self, f: Callable[[A], 'State[S, A]']) -> 'State[S, A]':
        def new_function(old_state: S) -> Tuple[A, S]:
            value, new_state = self.function(old_state)
            return f(value).function(new_state)
        return State(new_function)

    @staticmethod
    def unit(value: A) -> 'State[S, A]':
        return State(lambda state: (value, state))

    def run(self, state: S) -> Tuple[A, S]:
        return self.function(state)

def ls(directory: str) -> State:
    return State(lambda state: (os.listdir(directory), state))

def cat(filename: str) -> State:
    with open(filename, 'r') as file:
        file_content = file.read()
    return State(lambda state: (file_content, state))

def grep(pattern: str, text: str) -> State:
    return State.unit([line for line in text.split('\n') if re.search(pattern, line)])

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
