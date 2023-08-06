
# Monadic Shell Interface in Python

This project provides a monadic interface for executing shell commands in Python. The idea is to represent shell commands as functions that take a state (representing the state of the filesystem) and return a new state along with some result. These functions can be chained together using the `bind` method, which allows for easy composition of shell commands.

The current implementation includes Python equivalents of the following shell commands:

- `ls`: List the contents of a directory
- `cat`: Print the contents of a file
- `grep`: Search for a pattern in some text

## Usage

You can use this monadic shell interface in your own Python scripts by importing the `State` class and the shell command functions from `script.py`:

```python
from script import State, ls, cat, grep
```

You can then create a sequence of commands by calling these functions and chaining them together using the `bind` method. For example, to list the contents of the current directory, read the first file in the list, and then print the lines of that file that contain the word 'import', you could do:

```python
commands = ls('.').bind(lambda filenames: cat(filenames[0])).bind(lambda text: grep('import', text))
result, _ = commands.run('.')
print(result)
```

This will print a list of lines from the first file in the current directory that contain the word 'import'.

## REPL

This project also includes a REPL (Read-Eval-Print Loop) that allows you to use the monadic shell interface interactively. To start the REPL, run `repl.py`:

```python
python repl.py
```

You can then enter commands at the `>` prompt. The available commands are `ls`, `cat`, and `grep`. You can exit the REPL by typing `exit`.
