
from typing import Callable, Tuple, TypeVar, List
import os
import shutil
import re

S = TypeVar('S')  # The type of the state
A = TypeVar('A')  # The type of the value

class State:
    # The State monad encapsulates a stateful computation. It takes a function that takes a state and returns a new state and a value.
    def __init__(self, function: Callable[[S], Tuple[A, S]]):
        self.function = function

    # The bind method is used to chain together stateful computations. It takes a function that returns a new State object and applies it to the value produced by the current State object.
    def bind(self, f: Callable[[A], 'State[S, A]']) -> 'State[S, A]':
        def new_function(old_state: S) -> Tuple[A, S]:
            value, new_state = self.function(old_state)
            return f(value).function(new_state)
        return State(new_function)

    # The unit method is a convenience method that creates a new State object that leaves the state unchanged and returns the given value.
    @staticmethod
    def unit(value: A) -> 'State[S, A]':
        return State(lambda state: (value, state))

    # The run method runs the stateful computation with the given initial state and returns the resulting value and state.
    def run(self, state: S) -> Tuple[A, S]:
        return self.function(state)

print('Hello, monadic shell!')
