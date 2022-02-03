import unittest

from ricolisp import LispInterpreter

class TestBasics(unittest.TestCase):
    def test_basics(self):
        li = LispInterpreter()