from ply import yacc

from feel.ErrorPrinters import unexpected_token
from feel.lexer.TableLexer import TableLexer
from feel.parser import AST


# noinspection PyMethodMayBeStatic
class TableParser:
    tokens = TableLexer.tokens
    precedence = [
        ('left', 'comparison_p'),
        ('left', 'INSTANCE'),
        ('left', 'path_expression_p'),
    ]

    # 7
    def p_simple_positive_unary_test(self, p):
        """simple_positive_unary_test : endpoint
                                      | op_endpoint
                                      | interval"""
        p[0] = p[1]

    def p_op_endpoint(self, p):
        """op_endpoint : '<' endpoint
                       | GTE endpoint
                       | '>' endpoint
                       | LTE endpoint"""
        p[0] = {
            '<': AST.LtEp(p[2]),
            '<=': AST.LteEp(p[2]),
            '>': AST.GtEp(p[2]),
            '>=': AST.GteEp(p[2])
        }[p[1]]

    # 8
    def p_interval(self, p):
        """interval : interval_starts endpoint DOTS endpoint interval_ends"""
        p[0] = AST.Interval(p[1], p[2], p[4], p[5])

    # 9-10
    def p_interval_starts(self, p):
        """interval_starts : '(' %prec comparison_p
                           | ']' %prec comparison_p
                           | '[' %prec comparison_p"""
        p[0] = {
            '(': AST.OpenIntervalStart,
            ']': AST.OpenIntervalStart,
            '[': AST.ClosedIntervalStart
        }[p[1]]()

    # 11-12
    def p_interval_ends(self, p):
        """interval_ends : ')'
                         | '['
                         | ']'"""
        p[0] = {
            ')': AST.OpenIntervalEnd,
            '[': AST.OpenIntervalEnd,
            ']': AST.ClosedIntervalEnd
        }[p[1]]()

    # 15
    def p_positive_unary_test(self, p):
        """positive_unary_test : null
                               | simple_positive_unary_test"""
        p[0] = p[1]

    # 16
    def p_positive_unary_tests(self, p):
        """positive_unary_tests : many_positive_unary_tests"""
        p[0] = AST.PositiveUnaryTests(p[1])

    def p_many_positive_unary_tests(self, p):
        """many_positive_unary_tests : positive_unary_test more_positive_unary_tests"""
        p[0] = [p[1]] + p[2]

    def p_more_positive_unary_tests(self, p):
        """more_positive_unary_tests : empty_list empty_list
                                     | ',' many_positive_unary_tests"""
        p[0] = p[2]

    # 17
    def p_unary_tests(self, p):
        """unary_tests : positive_unary_tests
                       | not_positive_unary_tests
                       | no_tests"""
        p[0] = p[1]

    # 17b
    def p_not_positive_tests(self, p):
        """not_positive_unary_tests : NOT '(' positive_unary_tests ')'"""
        p[0] = AST.Not(p[3])

    # 17c
    def p_no_tests(self, p):
        """no_tests : '-'"""
        p[0] = AST.NoTest()

    # 18
    def p_endpoint(self, p):
        """endpoint : simple_value"""
        p[0] = AST.Endpoint(p[1])

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

    def p_null(self, p):
        """null : NULL"""
        p[0] = AST.Null()

    def p_error(self, p):
        if p:
            unexpected_token(p)
        else:
            print('unexpected end of file')

    def __init__(self, **kwargs) -> None:
        self.lexer = TableLexer()
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, *args, **kwargs):
        return self.parser.parse(*args, lexer=self.lexer.lexer, **kwargs)


parser = TableParser(start='unary_tests')
