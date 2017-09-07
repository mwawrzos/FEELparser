import unittest
from typing import Optional

from feel.parser import AST
from feel.parser.TableParser import parser


class TestTableParser(unittest.TestCase):
    def check_parser(self, str_input: str, ast: Optional[AST.AST], debug=False) -> None:
        self.assertEqual(parser.parse(str_input, debug=debug), ast)

    def no_test_unary_test(self):
        self.check_parser('null', AST.Null())
