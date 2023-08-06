
from typing import Callable, Tuple, TypeVar, List
import os
import shutil
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

def test_ls():
    commands = ls('.')
    result, state = commands.run('.')
    assert 'README.md' in result, "ls test failed"

def test_cat():
    commands = cat('README.md')
    result, state = commands.run('.')
    assert '# Monadic Shell Interface in Python' in result, "cat test failed"

def test_grep():
    commands = cat('README.md').bind(lambda text: grep('Monadic', text))
    result, state = commands.run('.')
    assert any('Monadic' in line for line in result), "grep test failed"

def run_tests():
    test_ls()
    test_cat()
    test_grep()

run_tests()
print("All tests passed.")
