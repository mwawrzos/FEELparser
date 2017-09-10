from ply.lex import LexToken
from ply.yacc import YaccSymbol


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


def missing_token_error(message, t):
    contextual_error(t, '%s; a token %s{%s} found instead' % (message, t.type, t.value))


def contextual_error(t, message):
    print(
        '%s at position %s:%s' % (message, t.lexpos - find_first_in_lane(t), t.lineno))
    print_context(t)


def token_repr(p):
    return '%s{%s}' % (p.type, p.value)


# noinspection PyPep8Naming
class UnexpectedError:
    def __call__(self, o):
        getattr(self, 'unexpected_%s' % o.type, 'unexpected')(o)

    @staticmethod
    def unexpected(o):
        unexpected(o)

    @staticmethod
    def unexpected_LexToken(o):
        unexpected_token(o)

    @staticmethod
    def unexpected_YaccSymbol(o):
        unexpected_symbol(o)


def unexpected_token(t):
    contextual_error(t, 'unexpected token %s' % token_repr(t))


def unexpected_symbol(p):
    contextual_error(p.value, 'unexpected symbol %s (token %s)' % (p.type, token_repr(p.value)))


def unexpected(_):
    print('something unexpected')
