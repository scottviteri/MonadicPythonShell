
from script import State, ls, cat, grep

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
