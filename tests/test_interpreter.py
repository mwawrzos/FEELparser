from unittest import TestCase

from FEELinterpreter import evaluate


class TestInterpreter(TestCase):
    def atest_in(self):
        self.assertEqual(evaluate('5 in (<=5)'), True)
