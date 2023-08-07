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

def resolve_path(state: str, path: str) -> str:
    if path == '.' or path == './':
        return state
    elif path == '..':
        return os.path.dirname(state)
    else:
        return path if os.path.isabs(path) else os.path.join(state, path)

def cd(directory: str) -> State:
    return State(lambda state: (None, resolve_path(state, directory)))

def ls(directory: str, type: str = 'both', include_hidden: bool = False) -> State:
    def filter_func(state: str, item: str) -> bool:
        resolved_path = resolve_path(state, item)
        if type == 'both':
            return True
        elif type == 'file':
            return os.path.isfile(resolved_path) and not item.endswith('.pyc')
        elif type == 'dir':
            return os.path.isdir(resolved_path) and item != '__pycache__'
        else:
            raise ValueError("type must be 'both', 'file', or 'dir'")

    def ls_func(state: str) -> Tuple[List[str], str]:
        items = os.listdir(resolve_path(state, directory))
        filtered_items = [item for item in items if filter_func(state, item) and (include_hidden or not item.startswith('.'))]
        return filtered_items, state

    return State(ls_func)

def cat(filename: str) -> State:
    return State(lambda state: (open(resolve_path(state, filename), 'r').read(), state))

def touch(filename: str) -> State:
    return State(lambda state: (open(resolve_path(state, filename), 'a').close(), state))

def rm(filename: str) -> State:
    return State(lambda state: (os.remove(resolve_path(state, filename)), state))

def grep(pattern: str, text: str) -> State:
    return State.unit([line for line in text.split('\n') if re.search(pattern, line)])

def pwd() -> State:
    return State(lambda state: (state, state))
