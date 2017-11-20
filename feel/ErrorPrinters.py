def find_first_in_lane(t):
    return t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1


def find_last_in_lane(t):
    last_newline = t.lexer.lexdata.find('\n', t.lexpos)
    if last_newline < 0:
        last_newline = len(t.lexer.lexdata)
    return last_newline - 1


def print_context(t, l):
    first_in_line = find_first_in_lane(t)
    last_in_line = find_last_in_lane(t)
    token_len = len(t.value) + 2 if t.type == 'STRING_LITERAL' else len(t.value)
    l.log(t.lexer.lexdata[first_in_line:last_in_line + 1])
    l.log('%s%s%s' % ('~' * (t.lexpos - first_in_line),
                      '^' * token_len,
                      '~' * (last_in_line - t.lexpos - token_len + 1)))


def missing_token_error(message, t, l):
    contextual_error(t, '%s; a token %s{%s} found instead' % (message, t.type, t.value), l)


def contextual_error(t, message, l):
    l.log(
        '%s at position %s:%s' % (message, t.lexpos - find_first_in_lane(t), t.lineno))
    print_context(t, l)


def token_repr(p):
    return '%s{%s}' % (p.type, p.value)


# noinspection PyPep8Naming
class UnexpectedError(object):
    def __call__(self, o, l):
        getattr(self, 'unexpected_%s' % type(o).__name__, self.unexpected)(o, l)

    @staticmethod
    def unexpected(o, l):
        unexpected(o, l)

    @staticmethod
    def unexpected_LexToken(o, l):
        unexpected_token(o, l)

    @staticmethod
    def unexpected_YaccSymbol(o, l):
        unexpected_symbol(o, l)


def unexpected_token(t, l):
    contextual_error(t, 'unexpected token %s' % token_repr(t), l)


def unexpected_symbol(p, l):
    contextual_error(p.value, 'unexpected symbol %s (token %s)' % (p.type, token_repr(p.value)), l)


def unexpected(_, l):
    l.log('something unexpected')


unexpected_error = UnexpectedError()
