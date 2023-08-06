# Monadic Shell Interface in Python

This project provides a monadic interface for executing shell commands in Python. The idea is to represent shell commands as functions that take a state (representing the state of the filesystem) and return a new state along with some result. These functions can be chained together using the bind method, which allows for easy composition of shell commands.

The current implementation includes Python equivalents of the following shell commands:

- ls: List the contents of a directory
- cat: Print the contents of a file
- grep: Search for a pattern in some text
- cd: Change the current directory
- pwd: Print the current directory
- touch: Create a new file
- rm: Remove a file

## Purpose and Motivation

The purpose of this project is to encapsulate stateful computations (in this case, shell commands that operate on the filesystem) in a way that allows them to be composed and run in a controlled manner. The state here is the current directory, and it's passed along and updated as commands are chained together.

This design allows you to build up complex sequences of stateful computations in a purely functional way, without any explicit state management. The state is implicitly managed by the State class and the bind method.

This design has several advantages:

- It makes the code easier to reason about, because the state is always explicit.
- It makes the code more modular, because stateful computations can be encapsulated in State objects and composed using bind.
- It makes the code more testable, because you can easily test individual commands with specific states.

## Usage

You can use this monadic shell interface in your own Python scripts by importing the State class and the shell command functions from script.py:

```python
from script import State, ls, cat, grep, cd, pwd, touch, rm
```
You can then create a sequence of commands by calling these functions and chaining them together using the bind method. For example, to list the contents of the current directory, read the first file in the list, and then print the lines of that file that contain the word 'import', you could do:

```python
commands = ls('.').bind(lambda filenames: cat(filenames[0])).bind(lambda text: grep('import', text))
result, _ = commands.run('.')
print(result)
```
This will print a list of lines from the first file in the current directory that contain the word 'import'.
Testing

The tests.py file includes tests for each of the shell command functions. Each test function takes the initial state (the current directory) as an argument, and run_tests gets the current working directory and passes it to each test function as the initial state.

For example, here's how the test_cd function checks that the cd function correctly changes the current directory:

```python
def test_cd(initial_state, new_state):
    commands = cd(new_state)
    _, state = commands.run(initial_state)
    assert state == new_state, "cd test failed"
```

In this test, cd(new_state) is expected to change the current directory to new_state. The test checks that the state returned by cd(new_state) is indeed new_state.

To run the tests, simply run tests.py:
```python
python tests.py
```

If all tests pass, it will print "All tests passed."

