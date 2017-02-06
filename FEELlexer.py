# coding=utf-8
from ply import lex

from FEEL_AST import Eq, Neq, Lt, Lte, Gt, Gte, SomeQuantifiedExpression, EveryQuantifiedExpression, Null

reserved = {
    'date': 'DATE',
    'time': 'TIME',
    'duration': 'DURATION',
    'function': 'FUNCTION',
    'and': 'AND',
    'or': 'OR',
    'external': 'EXTERNAL',
    'instance': 'INSTANCE',
    'of': 'OF',
    'between': 'BETWEEN',
    'in': 'IN',
    'satisfies': 'SATISFIES',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'for': 'FOR',
    'return': 'RETURN',
}

tokens = [
             'NAME',
             'STRING_LITERAL',
             'NUMERIC_LITERAL',
             'BOOLEAN_LITERAL',
             'EQ',
             'NEQ',
             'LT',
             'LTE',
             'GT',
             'GTE',
             'SOME',
             'EVERY',
             'EXPONENT',
             'NULL',
         ] + reserved.values()

literals = "()[]{}:.,=+-*/"

t_ignore = r' '

t_EXPONENT = r'\*\*'

ADDITIONAL_NAME_SYMBOLS = ur'[\./\-’\+\*]'
NAME_START_CHAR = ur'[\?A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD]'
NAME_PART_CHAR = r'(' + NAME_START_CHAR + ur'| \d | [\u00B7\u0300-\u036F\u203F-\u2040])'
NAME_PART = NAME_PART_CHAR + r'+'
NAME_START = NAME_START_CHAR + NAME_PART_CHAR + r'+'
t_NAME = NAME_START + r'(' + NAME_PART + ADDITIONAL_NAME_SYMBOLS + r')*'
PARAMETER_NAME = t_NAME
FORMAL_PARAMETER = PARAMETER_NAME


def t_NUMERIC_LITERAL(t):
    r'(\d+(\.\d+)?|\.\d+)'
    t.value = float(t.value)
    return t


def t_BOOLEAN_LITERAL(t):
    r'(true|false)'
    t.value = t.value == 'true'
    return t


def t_STRING_LITERAL(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_EQ(t):
    r'='
    t.value = Eq
    return t


def t_NEQ(t):
    r'!='
    t.value = Neq
    return t


def t_LTE(t):
    r'<='
    t.value = Lte
    return t


def t_LT(t):
    r'<'
    t.value = Lt
    return t


def t_GTE(t):
    r'>='
    t.value = Gte
    return t


def t_GT(t):
    r'>'
    t.value = Gt
    return t


def t_SOME(t):
    r'some'
    t.value = SomeQuantifiedExpression
    return t


def t_EVERY(t):
    r'every'
    t.value = EveryQuantifiedExpression
    return t


def t_NULL(t):
    r'null'
    t.value = Null()
    return t


def t_NAME2(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')

    return t


def t_error(t):
    print "Ill char: '%s'" % t.value[0]
    t.lexer.skip(1)


lexer = lex.lex()
