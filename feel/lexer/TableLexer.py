import re

from ply import lex

from feel.ErrorPrinters import print_context, find_first_in_lane
from feel.lexer.BaseLexer import NAME


# noinspection PyPep8Naming,PyMethodMayBeStatic
from utils.PrintLogger import PrintLogger


# noinspection PyMethodMayBeStatic
class TableLexer(object):
    reserved = {
        'date': 'DATE',
        'time': 'TIME',
        'date and time': 'DATE_AND_TIME',
        'duration': 'DURATION',
        'true': 'TRUE',
        'false': 'FALSE',
        'not': 'NOT',
        'null': 'NULL',
    }

    tokens = [
                 'STRING_LITERAL',
                 'NUMERIC_LITERAL',
                 'NAME',
                 'NEWLINE',
                 'GTE',
                 'LTE',
                 'DOTS',
             ] + list(reserved.values())

    literals = '()-,'

    t_ignore = ' \t'

    t_GTE = r'>='
    t_LTE = r'<='
    t_DOTS = r'\.\.'

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

    def t_error(self, t):
        self.logger.log("Unexpected character: '%s'" % t.value[0],
                        'at position %d:%d' % (t.lexer.lexpos - find_first_in_lane(t), t.lexer.lineno))
        print_context(t, self.logger)
        t.lexer.skip(1)

    def t_NAME(self, t):
        t.type = TableLexer.reserved.get(t.value, 'NAME')

        return t

    t_NAME.__doc__ = NAME

    def __init__(self, logger=PrintLogger(), **kwargs):
        self.logger = logger
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()
