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
    return State(lambda state: (os.listdir(os.path.join(state, directory)), state))

def cat(filename: str) -> State:
    return State(lambda state: (open(os.path.join(state, filename), 'r').read(), state))

def grep(pattern: str, text: str) -> State:
    return State.unit([line for line in text.split('\n') if re.search(pattern, line)])

def cd(directory: str) -> State:
    return State(lambda state: (None, os.path.join(state, directory)))

def pwd() -> State:
    return State(lambda state: (state, state))

def touch(filename: str) -> State:
    return State(lambda state: (open(os.path.join(state, filename), 'a').close(), state))

def rm(filename: str) -> State:
    return State(lambda state: (os.remove(os.path.join(state, filename)), state))