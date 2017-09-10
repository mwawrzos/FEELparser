# encoding: utf8
import re
from ply import lex

from feel.ErrorPrinters import print_context, find_first_in_lane

ADDITIONAL_NAME_SYMBOLS = r'[\./\-’\+\*]'
NAME_START_CHAR = r'[\?A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070' \
                  r'-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\U00010000-\U000EFFFF]'
NAME_PART_CHAR = r'(' + NAME_START_CHAR + r'| \d | [\u00B7\u0300-\u036F\u203F-\u2040])'
NAME_PART = NAME_PART_CHAR + r'+'
NAME_START = NAME_START_CHAR + NAME_PART_CHAR + r'*'
NAME = NAME_START + r'(\s?(' + NAME_PART + r'|' + ADDITIONAL_NAME_SYMBOLS + r'))*'


# noinspection PyMethodMayBeStatic,PyPep8Naming
class BaseLexer:
    reserved = {
        'date': 'DATE',
        'time': 'TIME',
        'date and time': 'DATE_AND_TIME',
        'duration': 'DURATION',
        'true': 'TRUE',
        'false': 'FALSE',
    }

    tokens = [
                 'NAME',
                 'STRING_LITERAL',
                 'NUMERIC_LITERAL',
                 'NEQ',
                 'LTE',
                 'GTE',
                 'NEWLINE',
                 'EXPONENT',
             ] + list(reserved.values())

    literals = '()[]{}:.,=+-*/<>'

    t_ignore = ' \t'

    t_GTE = '>='
    t_LTE = '<='
    t_NEQ = '!='
    t_EXPONENT = r'\*\*'

    def t_NEWLINE(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    def t_STRING_LITERAL(self, t):
        r""""[^"]*\""""
        t.value = t.value[1:-1]
        return t

    def t_NUMERIC_LITERAL(self, t):
        r"""(\d+\s*(\.\s*\d+)?|\.\s*\d+)"""
        t_value = re.sub('\s', '', str(t.value))
        t.value = float(t_value)
        return t

    def t_NAME(self, t):
        t.type = BaseLexer.reserved.get(t.value, 'NAME')

        return t

    t_NAME.__doc__ = NAME

    def t_error(self, t):
        print("Unexpected character: '%s'" % t.value[0],
              'at position %d:%d' % (t.lexer.lexpos - find_first_in_lane(t), t.lexer.lineno))
        print_context(t)
        t.lexer.skip(1)

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()
