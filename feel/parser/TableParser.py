from ply import yacc

# noinspection PyUnresolvedReferences
from FEELlexer import tokens

# noinspection PyUnresolvedReferences
from feel.parser.Parser import p_positive_unary_tests, p_error


def p_unary_tests(p):
    """unary_tests : positive_unary_tests"""
    p[0] = p[1]

parser = yacc.yacc()
