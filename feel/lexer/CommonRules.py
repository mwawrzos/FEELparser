import re

from ply import lex


def find_first_in_lane(t):
    return t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1


def find_last_in_lane(t):
    last_newline = t.lexer.lexdata.find('\n', t.lexpos)
    if last_newline < 0:
        last_newline = len(t.lexer.lexdata)
    return last_newline - 1


def print_context(t):
    first_in_line = find_first_in_lane(t)
    last_in_line = find_last_in_lane(t)
    token_len = len(t.value) + 2 if t.type == 'STRING_LITERAL' else len(t.value)
    print(t.lexer.lexdata[first_in_line:last_in_line + 1])
    print('%s%s%s' % ('~' * (t.lexpos - first_in_line),
                      '^' * token_len,
                      '~' * (last_in_line - t.lexpos - token_len + 1)))


# noinspection PyMethodMayBeStatic
class CommonRules(object):
    reserved = {
        'date': 'DATE',
        'time': 'TIME',
        'date and time': 'DATE_AND_TIME',
        'duration': 'DURATION',
        'function': 'FUNCTION',
        'external': 'EXTERNAL',
        'and': 'AND',
        'or': 'OR',
        'instance': 'INSTANCE',
        'of': 'OF',
        'between': 'BETWEEN',
        'null': 'NULL',
        'in': 'IN',
        'some': 'SOME',
        'every': 'EVERY',
        'satisfies': 'SATISFIES',
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'for': 'FOR',
        'return': 'RETURN',
        'true': 'TRUE',
        'false': 'FALSE',
        'not': 'NOT',
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
                 'DOTS',
             ] + list(reserved.values())

    literals = '()[]{}:.,=+-*/<>'

    t_ignore = ' \t'

    def t_NEWLINE(self, t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    t_EXPONENT = r'\*\*'
    t_DOTS = r'\.\.'

    ADDITIONAL_NAME_SYMBOLS = r'[\./\-’\+\*]'
    NAME_START_CHAR = r'[\?A-Z_a-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070'\
                      r'-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\U00010000-\U000EFFFF]'
    NAME_PART_CHAR = r'(' + NAME_START_CHAR + r'| \d | [\u00B7\u0300-\u036F\u203F-\u2040])'
    NAME_PART = NAME_PART_CHAR + r'+'
    NAME_START = NAME_START_CHAR + NAME_PART_CHAR + r'*'
    NAME = NAME_START + r'(\s?(' + NAME_PART + r'|' + ADDITIONAL_NAME_SYMBOLS + r'))*'

    def t_NUMERIC_LITERAL(self, t):
        r"""(\d+\s*(\.\s*\d+)?|\.\s*\d+)"""
        t_value = re.sub('\s', '', str(t.value))
        t.value = float(t_value)
        return t

    def t_STRING_LITERAL(self, t):
        r""""[^"]*\""""
        t.value = t.value[1:-1]
        return t

    t_NEQ = '!='
    t_LTE = '<='
    t_GTE = '>='

    def t_NAME(self, t):
        t.type = CommonRules.reserved.get(t.value, 'NAME')

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
