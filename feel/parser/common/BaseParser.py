from ply import yacc

from feel.ErrorPrinters import unexpected_token
from feel.lexer.BaseLexer import BaseLexer as Lexer
from feel.parser import AST


# noinspection PyMethodMayBeStatic
class BaseParser:
    tokens = Lexer.tokens

    precedence = [
        ('left', '=', '<', 'LTE', '>', 'GTE'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'EXPONENT'),
        ('right', 'negation_p'),
        ('left', 'INSTANCE'),
        ('left', 'path_expression_p'),
    ]

    # 1
    # rule overridden by concrete parsers
    # cases are only for removing 'unused rule' warnings
    def p_expression(self, p):
        """expression : '1' arithmetic_expression
                      | '3' empty_list
                      | '4' comparison
                      | '5' simple_value"""

    # 4
    def p_arithmetic_expression(self, p):
        """arithmetic_expression : binary_operators
                                 | arithmetic_negation"""
        p[0] = p[1]

    # 19
    def p_simple_value(self, p):
        """simple_value : qualified_name
                        | simple_literal"""
        p[0] = p[1]

    # 20
    def p_qualified_name(self, p):
        """qualified_name : name dot_names"""
        p[0] = [p[1]] + p[2]

    def p_dot_names(self, p):
        """dot_names :                    %prec INSTANCE
                     | '.' name dot_names %prec path_expression_p"""
        p[0] = [p[2]] + p[3] if len(p.slice) == 4 else []

    # 21-25
    def p_binary_operators(self, p):
        """binary_operators : expression '+'      expression
                            | expression '-'      expression
                            | expression '*'      expression
                            | expression '/'      expression
                            | expression EXPONENT expression"""
        operators = {
            '+': AST.Sum,
            '-': AST.Dif,
            '*': AST.Mul,
            '/': AST.Div,
            '**': AST.Exp
        }
        p[0] = operators[p[2]](p[1], p[3])

    # 26
    def p_arithmetic_negation(self, p):
        """arithmetic_negation : '-' expression %prec negation_p"""
        p[0] = AST.Negation(p[2])

    # 27-32
    def p_name(self, p):
        """name : NAME"""
        p[0] = AST.Name(p[1])

    # 34
    def p_simple_literal(self, p):
        """simple_literal : numeric_literal
                          | string_literal
                          | boolean_literal
                          | date_time_literal"""
        p[0] = p[1]

    # 35
    def p_string_literal(self, p):
        """string_literal : STRING_LITERAL"""
        p[0] = AST.StringLiteral(p[1])

    # 36
    def p_boolean_literal(self, p):
        """boolean_literal : TRUE
                           | FALSE"""
        p[0] = AST.Boolean(p[1] == 'true')

    # 37-39
    def p_numeric_literal(self, p):
        """numeric_literal : NUMERIC_LITERAL"""
        p[0] = AST.Number(p[1])

    # 51
    def p_comparison(self, p):
        """comparison : operator"""
        p[0] = p[1]

    # 51a
    def p_operator(self, p):
        """operator : expression '=' expression
                    | expression NEQ expression
                    | expression '<' expression
                    | expression LTE expression
                    | expression '>' expression
                    | expression GTE expression"""
        p[0] = {
            '=': AST.Eq,
            '!=': AST.Neq,
            '<': AST.Lt,
            '<=': AST.Lte,
            '>': AST.Gt,
            '>=': AST.Gte
        }[p[2]](p[1], p[3])

    # 62
    def p_date_time_literal(self, p):
        """date_time_literal : DATE          '(' STRING_LITERAL ')'
                             | TIME          '(' STRING_LITERAL ')'
                             | DATE_AND_TIME '(' STRING_LITERAL ')'
                             | DATE_AND_TIME '(' STRING_LITERAL NEWLINE ')'
                             | DURATION      '(' STRING_LITERAL ')'"""
        p[0] = {
            'date': AST.Date,
            'time': AST.Time,
            'date and time': AST.DateAndTime,
            'duration': AST.Duration
        }[p[1]](p[3])

    # helper rules
    def p_empty_list(self, p):
        """empty_list : """
        p[0] = []

    def p_error(self, p):
        if p:
            unexpected_token(p)
        else:
            print('unexpected end of file')

    def __init__(self, **kwargs) -> None:
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, *args, **kwargs):
        return self.parser.parse(*args, lexer=self.lexer.lexer, **kwargs)


parser = BaseParser()
