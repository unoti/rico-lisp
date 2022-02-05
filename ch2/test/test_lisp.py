import unittest

from ricolisp import LispInterpreter
from ricolisp.interpreter import tokenize, parse, standard_env

class TestConsole:
    def __init__(self):
        self.pending_input = [] # Things the user has typed.
        self.pending_output = [] # Things waiting to be printed.
        self.expectations = [] # A queue of things we expect to see in the output.

    # -- input() and print() are used by the lisp interpreter.
    def input(self, prompt: str):
        # When we don't have any input left then type 'exit'.
        if len(self.pending_input) == 0:
            return 'exit'
        return self.pending_input.pop(0) # Remove the first item from the queue.

    def print(self, value):
        """Print output to the console."""
        self.pending_output.append(value)
    
    # -- enter() and read() are used by the unit tests.
    def enter(self, s: str):
        """Type something into this console."""
        self.pending_input.append(s)
    
    def read(self):
        """Get a line of output from the console."""
        if len(self.pending_output) == 0:
            return None
        return self.pending_output.pop(0)
    
    def expect(self, v):
        """Log that we expect to see the given value appear in the output."""
        self.expectations.append(v)
    
    def verify_expectations(self, test_case):
        """Verify that the console received each of the expected outputs."""
        test_case.assertListEqual(self.expectations, self.pending_output)

class TestLisp(unittest.TestCase):
    def test_tokenize(self):
        source_code = "(begin (define r 10) (* pi (* r r)))"
        expected_tokens = ['(', 'begin', '(', 'define', 'r', '10', ')',
            '(', '*', 'pi', '(', '*', 'r', 'r', ')', ')', ')']

        tokens = tokenize(source_code)
        self.assertListEqual(expected_tokens, tokens)

    def test_parse(self):
        source_code = '(begin (define r 10) (* pi (* r r)))'
        expression = parse(source_code)
        expected_expression = ['begin', ['define', 'r', 10], ['*', 'pi', ['*', 'r', 'r']]]
        self.assertListEqual(expected_expression, expression)

    def test_standard_environment(self):
        env = standard_env()

    def test_interpreter(self):
        lisp = LispInterpreter()
        source_code = '(begin (define r 10) (* pi (* r r)))'
        result = lisp.run(source_code)
        self.assertAlmostEqual(314.15926535, result, places=5)
    
    def test_repl(self):
        console = TestConsole()
        lisp = LispInterpreter()
        console.enter('(+ 5 15)')
        console.expect(20)
        console.enter('(+ 1 (* 5 10))')
        console.expect(51)
        lisp.repl(console=console)
        console.verify_expectations(self)
