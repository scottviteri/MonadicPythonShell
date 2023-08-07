import os
from script import *

def test_ls(initial_state):
    commands = ls('.')
    result, state = commands.run(initial_state)
    assert state == initial_state, "ls test failed"
    assert isinstance(result, list), "ls test failed"

def test_cd(initial_state):
    commands = cd(initial_state)
    _, state = commands.run(initial_state)
    assert state == initial_state, "cd test failed"

def test_cat(initial_state):
    commands = ls('.', 'file').bind(lambda files: cat(files[0]))
    result, state = commands.run(initial_state)
    assert state == initial_state, "cat test failed"
    assert isinstance(result, str), "cat test failed"

def test_grep(initial_state):
    commands = ls('.', 'file').bind(lambda files: cat(files[0])).bind(lambda text: grep('import', text))
    result, state = commands.run(initial_state)
    assert state == initial_state, "grep test failed"
    assert isinstance(result, list), "grep test failed"

def test_pwd(initial_state):
    commands = pwd()
    result, state = commands.run(initial_state)
    assert state == initial_state, "pwd test failed"
    assert result == initial_state, "pwd test failed"

def test_touch_rm(initial_state):
    commands = touch('test_file.txt').bind(lambda _: rm('test_file.txt'))
    _, state = commands.run(initial_state)
    assert state == initial_state, "touch/rm test failed"
    assert not os.path.exists(os.path.join(initial_state, 'test_file.txt')), "touch/rm test failed"

#def test_complex_example(initial_state):
#    commands = ls('.', 'dir').bind(
#        lambda dirs: cd(dirs[0]) if dirs else pwd()
#    ).bind(
#        lambda _: ls('.', 'file')
#    ).bind(
#        lambda files: cat(files[0]) if files else pwd()
#    ).bind(
#        lambda text: grep('import', text) if text else pwd()
#    ).bind(
#        lambda _: cd('..')
#    ).bind(
#        lambda _: touch('new_file.txt')
#    ).bind(
#        lambda _: pwd()
#    )
#    result, state = commands.run(initial_state)
#    assert state == initial_state, "complex example test failed"
#    assert os.path.exists(os.path.join(initial_state, 'new_file.txt')), "complex example test failed"
#
def run_tests():
    initial_state = os.getcwd()
    test_ls(initial_state)
    test_cd(initial_state)
    test_cat(initial_state)
    test_grep(initial_state)
    test_pwd(initial_state)
    test_touch_rm(initial_state)
    #test_complex_example(initial_state)
    print("All tests passed.")

if __name__ == "__main__":
    run_tests()