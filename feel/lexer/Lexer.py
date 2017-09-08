from feel.lexer.BaseLexer import BaseLexer


# noinspection PyPep8Naming
class Lexer(BaseLexer):
    reserved = BaseLexer.reserved
    new_reserved = {
        'function': 'FUNCTION',
        'external': 'EXTERNAL',
        'and': 'AND',
        'or': 'OR',
        'instance': 'INSTANCE',
        'of': 'OF',
        'between': 'BETWEEN',
        'in': 'IN',
        'some': 'SOME',
        'every': 'EVERY',
        'satisfies': 'SATISFIES',
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'for': 'FOR',
        'return': 'RETURN',
        'null': 'NULL',
    }
    reserved.update(new_reserved)

    tokens = BaseLexer.tokens + [
        'DOTS',
    ] + list(new_reserved.values())

    t_DOTS = r'\.\.'
