
# Monadic Shell Interface in Python

This repository contains a Python script that demonstrates a monadic interface for shell-like commands.

The script defines a State monad and a set of commands that return State objects. These commands can be chained together using the bind method to create sequences of commands that pass their output from one command to the next.

This interface provides a flexible and powerful way to compose and execute shell-like commands in Python.

## How to Use

1. Define a set of commands as functions that return State objects. Each command should take its inputs as arguments and return a new State object that encapsulates a stateful computation.

```python
def ls(directory: str) -> State:
    return State(lambda state: (os.listdir(directory), state))

def cat(filename: str) -> State:
    return State(lambda state: (open(filename, 'r').readlines(), state))

def grep(pattern: str, text: List[str]) -> State:
    return State.unit([line for line in text if re.search(pattern, line)])
```

2. Compose these commands using the bind method to create a sequence of commands. The bind method takes a function that returns a new State object and applies it to the value produced by the current State object.

```python
commands = ls('.').bind(lambda filenames: cat(filenames[0])).bind(lambda lines: grep('import', lines))
```

3. Run the composed commands with an initial state using the run method.

```python
result = commands.run('.')
```

## Running Tests

This repository also includes a set of test cases that demonstrate the functionality of the monadic shell interface. To run these tests, execute the script `tests.py`:

```bash
python tests.py
```

If all tests pass, the script will print "All tests passed." If any test fails, the script will print an error message and exit with a non-zero status code.
