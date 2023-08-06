from script import State, ls, cat, grep, cd, pwd, touch, rm
import os

def test_ls(initial_state):
    commands = ls('.')
    result, state = commands.run(initial_state)
    assert 'README.md' in result, "ls test failed"

def test_cat(initial_state):
    commands = cat('README.md')
    result, state = commands.run(initial_state)
    assert '# Monadic Shell Interface in Python' in result, "cat test failed"

def test_grep(initial_state):
    commands = cat('README.md').bind(lambda text: grep('Monadic', text))
    result, state = commands.run(initial_state)
    assert any('Monadic' in line for line in result), "grep test failed"

def test_cd(initial_state, new_state):
    commands = cd(new_state)
    _, state = commands.run(initial_state)
    assert state == new_state, "cd test failed"

def test_pwd(initial_state):
    commands = pwd()
    result, state = commands.run(initial_state)
    assert result == initial_state, "pwd test failed"

def test_touch(initial_state):
    commands = touch('testfile')
    _, state = commands.run(initial_state)
    assert 'testfile' in os.listdir(initial_state), "touch test failed"
    rm('testfile').run(initial_state)  # cleanup

def test_rm(initial_state):
    touch('testfile').run(initial_state)  # setup
    commands = rm('testfile')
    _, state = commands.run(initial_state)
    assert 'testfile' not in os.listdir(initial_state), "rm test failed"

def run_tests():
    initial_state = os.getcwd()
    new_state = os.path.dirname(initial_state)
    test_ls(initial_state)
    test_cat(initial_state)
    test_grep(initial_state)
    test_cd(initial_state, new_state)
    test_pwd(initial_state)
    test_touch(initial_state)
    test_rm(initial_state)

run_tests()

print("All tests passed.")