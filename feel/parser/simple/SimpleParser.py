from feel.lexer.BaseLexer import BaseLexer
from feel.parser import AST
from feel.parser.common.BaseParser import BaseParser


# noinspection PyMethodMayBeStatic
class SimpleParser(BaseParser):
    tokens = BaseLexer.tokens

    precedence = [
        ('left', '=', 'NEQ', '<', 'LTE', '>', 'GTE'),
        ('left', ','),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'EXPONENT'),
        ('right', 'negation_p'),
        ('left', 'INSTANCE'),
        ('left', 'path_expression_p'),
        ('right', '.'),
    ]

    # 1
    def p_expression(self, p):
        """expression : simple_expression"""
        p[0] = p[1]

    # 5
    def p_simple_expression(self, p):
        """simple_expression : arithmetic_expression
                             | simple_value
                             | comparison"""
        p[0] = p[1]

    # 6
    def p_simple_expressions(self, p):
        """simple_expressions : many_simple_expressions"""
        p[0] = AST.SimpleExpressions(p[1])

    def p_many_simple_expressions(self, p):
        """many_simple_expressions : expression more_simple_expressions"""
        p[0] = [p[1]] + p[2]

    def p_more_simple_expressions(self, p):
        """more_simple_expressions : empty_list empty_list
                                   | ',' many_simple_expressions"""
        p[0] = p[2]


parser = SimpleParser(start='simple_expressions')
