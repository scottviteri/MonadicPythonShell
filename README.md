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
>>> from script import State, ls, cat, grep, cd, pwd, touch, rm

>>> ls('.').run(os.getcwd())
(['tests.py', 'LICENSE', '.git', 'script.py', 'repl.py', '__pycache__', 'README.md'], '/home/scottviteri/Projects/MonadicPythonShell')
```

The function ls('.').run(os.getcwd()) is an example of how to use the monadic shell interface provided by this project.

The ls function is a Python equivalent of the shell command ls, which lists the contents of a directory. It takes a directory as an argument and returns a State object representing a computation that, when run, will return the contents of the directory and the new state.

The run method is used to execute the computation represented by a State object. It takes an initial state as an argument and returns a tuple containing the result of the computation and the new state.

In the function ls('.').run(os.getcwd()), the initial state is the current working directory, obtained by calling os.getcwd(). The ls('.') computation is then run with this initial state, resulting in a tuple containing the contents of the current directory and the new state (which is the same as the initial state, because ls doesn't change the state).

You can then create a sequence of commands by calling these functions and chaining them together using the bind method. For example, to list the contents of the current directory, read the first file in the list, and then print the lines of that file that contain the word 'import', you could do:

```python
commands = ls('.').bind(lambda filenames: cat(filenames[0])).bind(lambda text: grep('import', text))
result, _ = commands.run(os.getcwd())
print(result)
```
This will print a list of lines from the first file in the current directory that contain the word 'import'.

Let's break down the control flow of the above commands:

1. `ls('.')`: This command lists the contents of the current directory. The '.' represents the current directory. This command returns a State object that, when run, will return a list of filenames in the current directory and the new state.

2. `.bind(lambda filenames: cat(filenames[0]))`: The bind method is used to chain together commands. It takes a function as an argument, which is applied to the result of the previous command. In this case, the function takes the list of filenames returned by `ls('.')` and reads the first file in the list using the `cat` command. This returns a new State object that, when run, will return the contents of the first file and the new state.

3. `.bind(lambda text: grep('import', text))`: This is another call to the bind method. The function passed to bind takes the text returned by `cat(filenames[0])` and searches for lines that contain the word 'import' using the `grep` command. This returns a new State object that, when run, will return a list of lines that contain 'import' and the new state.

4. `commands.run(os.getcwd())`: This runs the sequence of commands with the initial state, which is the current working directory obtained by calling `os.getcwd()`. This returns a tuple containing the result of the last command in the sequence and the final state.

5. `print(result)`: This prints the result of the last command in the sequence, which is a list of lines from the first file in the current directory that contain the word 'import'.

So, the control flow of these commands is a sequence of stateful computations, where each computation is dependent on the result of the previous computation. The state (the current directory) is passed along and updated as commands are chained together using the bind method.



## Testing

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

## More Examples

Here's a more complex example that demonstrates the power of this monadic shell interface. This example will:

1. List the contents of the current directory.
2. Change to the first directory in the list.
3. List the contents of that directory.
4. Read the first file in that list.
5. Print the lines of that file that contain the word 'import'.
6. Change back to the parent directory.
7. Create a new file in the parent directory.
8. Print the current directory.

Here's the command sequence:
```python
commands = ls('.', 'dir').bind(
    lambda dirs: cd(dirs0])).bind(
    lambda : ls('.', 'file')).bind(
    lambda files: cat(files0])).bind(
    lambda text: grep('import', text)).bind(
    lambda : cd('..')).bind(
    lambda : touch('new_file.txt')).bind(
    lambda : pwd())
    result, = commands.run(os.getcwd())
print(result)
````


Here's another example of a sequence of commands that would be difficult to do without this monadic interface. This sequence of commands lists the contents of the current directory, changes to the first directory in the list, creates a new file in that directory, and then prints the current directory:

```python
commands = ls('.').bind(lambda dirs: cd(dirs[0])).bind(lambda _: touch('new_file.txt')).bind(lambda _: pwd())
result, _ = commands.run('.')
print(result)
```


