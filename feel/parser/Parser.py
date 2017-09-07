from ply import yacc

# noinspection PyUnresolvedReferences
from FEELlexer import tokens, lexer, print_context, find_first_in_lane
from feel.parser import AST

precedence = [
    ('right', 'function_definition_p', 'quantified_p', 'if_p', 'for_p'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', '=', 'NEQ', '<', 'LTE', '>', 'GTE'),
    ('left', 'BETWEEN'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', 'EXPONENT'),
    ('right', 'negation_p'),
    ('left', 'INSTANCE'),
    ('left', 'path_expression_p'),
    ('right', '.'),
    ('left', '[')
]


def create_literal(name, *args):
    literals = {
        'date': AST.Date,
        'time': AST.Time,
        'date and time': AST.DateAndTime,
        'duration': AST.Duration
    }
    return literals[name](*args)


# 1
def p_expression(p):
    """expression : textual_expression
                  | boxes_expression"""
    p[0] = p[1]


# 2
def p_textual_expression(p):
    """textual_expression : for_expression
                          | if_expression
                          | quantified_expression
                          | disjunction
                          | conjunction
                          | comparison
                          | arithmetic_expression
                          | instance_of
                          | path_expression
                          | filter_expression
                          | function_invocation
                          | literal
                          | name"""
    p[0] = p[1]


# 4
def p_arithmetic_expression(p):
    """arithmetic_expression : exponentiation
                             | arithmetic_negation"""
    p[0] = p[1]


# 5
def p_simple_expression(p):
    """simple_expression : simple_value"""
    p[0] = p[1]


# 15
def p_positive_unary_test(p):
    """positive_unary_test : NULL"""
    p[0] = AST.Null()


# 16
def p_positive_unary_tests(p):
    """positive_unary_tests : many_positive_unary_tests"""
    p[0] = AST.PositiveUnaryTests(p[1])


def p_many_positive_unary_tests(p):
    """many_positive_unary_tests : positive_unary_test more_positive_unary_tests"""
    p[0] = [p[1]] + p[2]


def p_more_positive_unary_tests(p):
    """more_positive_unary_tests : empty_list empty_list
                                 | ',' many_positive_unary_tests"""
    p[0] = p[2]


# 17
def p_unary_tests(p):
    """unary_tests : positive_unary_tests
                   | not_positive_unary_tests
                   | no_tests"""
    p[0] = p[1]


# 17b
def p_not_positive_tests(p):
    """not_positive_unary_tests : NOT '(' positive_unary_tests ')'"""
    p[0] = AST.Not(p[3])


# 17c
def p_no_tests(p):
    """no_tests : '-'"""
    p[0] = AST.NoTest()


# 19
def p_simple_value(p):
    """simple_value : qualified_name
                    | simple_literal"""
    p[0] = p[1]


# 20
def p_qualified_name(p):
    """qualified_name : name dot_names"""
    p[0] = [p[1]] + p[2]


def p_dot_names(p):
    """dot_names :                    %prec INSTANCE
                 | '.' name dot_names %prec path_expression_p"""
    p[0] = [p[2]] + p[3] if len(p.slice) == 4 else []


# 21-25
def p_exponentiation(p):
    """exponentiation : expression '+'      expression
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
def p_arithmetic_negation(p):
    """arithmetic_negation : '-' expression %prec negation_p"""
    p[0] = AST.Negation(p[2])


# 27-32
def p_name(p):
    """name : NAME"""
    p[0] = AST.Name(p[1])


# 33
def p_literal(p):
    """literal : simple_literal
               | null"""
    p[0] = p[1]


# 34
def p_simple_literal(p):
    """simple_literal : numeric_literal
                      | string_literal
                      | boolean_literal
                      | date_time_literal"""
    p[0] = p[1]


# 35
def p_string_literal(p):
    """string_literal : STRING_LITERAL"""
    p[0] = AST.StringLiteral(p[1])


# 36
def p_boolean_literal(p):
    """boolean_literal : TRUE
                       | FALSE"""
    p[0] = AST.Boolean(p[1] == 'true')


# 37-39
def p_numeric_literal(p):
    """numeric_literal : NUMERIC_LITERAL"""
    p[0] = AST.Number(p[1])


# 40
def p_function_invocation(p):
    """function_invocation : expression parameters"""
    p[0] = AST.Invocation(p[1], p[2])


# 41
def p_parameters(p):
    """parameters : '(' positional_parameters ')'
                  | '(' named_parameters      ')'"""
    p[0] = p[2]


# 42
def p_named_parameters(p):
    """named_parameters : one_param_pair
                        | many_param_pairs"""
    p[0] = p[1]


def p_one_param_pair(p):
    """one_param_pair : parameter_name ':' expression"""
    p[0] = [(p[1], p[3])]


def p_many_param_pairs(p):
    """many_param_pairs : one_param_pair ',' named_parameters"""
    p[0] = p[1] + p[3]


# 43
def p_parameter_name(p):
    """parameter_name : name"""
    p[0] = p[1]


# 44
def p_positional_parameters(p):
    """positional_parameters : expressions
                             | empty_list"""
    p[0] = p[1]


def p_expressions(p):
    """expressions : single_expression
                   | many_expressions"""
    p[0] = p[1]


def p_single_expression(p):
    """single_expression : expression"""
    p[0] = [p[1]]


def p_many_expressions(p):
    """many_expressions : single_expression ',' expressions"""
    p[0] = p[1] + p[3]


# 45
def p_path_expression(p):
    """path_expression : expression '.' name"""
    p[0] = AST.Path(p[1], p[3])


# 46
def p_for_expression(p):
    """for_expression : FOR in_pairs RETURN expression %prec for_p"""
    p[0] = AST.For(p[2], p[4])


# 47
def p_if_expression(p):
    """if_expression : IF expression THEN expression ELSE expression %prec if_p"""
    p[0] = AST.If(p[2], p[4], p[6])


# 48
def p_quantified_expression(p):
    """quantified_expression : SOME  in_pairs SATISFIES expression %prec quantified_p
                             | EVERY in_pairs SATISFIES expression %prec quantified_p"""
    p[0] = AST.QuantifiedExpr(p.slice[1].type == 'SOME', p[2], p[4])


def p_in_pairs(p):
    """in_pairs : one_in_pair
                | many_in_pairs"""
    p[0] = p[1]


def p_one_in_pair(p):
    """one_in_pair : name IN expression"""
    p[0] = [(p[1], p[3])]


def p_many_in_pairs(p):
    """many_in_pairs : one_in_pair in_pairs"""
    p[0] = p[1] + p[2]


# 49
def p_disjunction(p):
    """disjunction : expression OR expression"""
    p[0] = AST.Disjunction(p[1], p[3])


# 50
def p_conjunction(p):
    """conjunction : expression AND expression"""
    p[0] = AST.Conjunction(p[1], p[3])


# 51
def p_comparison(p):
    """comparison : operator
                  | between
                  | in1
                  | in2"""
    p[0] = p[1]


# 51a
def p_operator(p):
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


# 51b
def p_between(p):
    """between : between1 AND expression"""
    expr, begin_start = p[1]
    begin_end = p[3]
    p[0] = AST.Between(expr, begin_start, begin_end)


def p_between1(p):
    """between1 : expression BETWEEN expression"""
    p[0] = p[1], p[3]


# 51c
def p_in1(p):
    """in1 : expression IN positive_unary_test"""
    p[0] = AST.In(p[1], AST.PositiveUnaryTests([p[3]]))


# 51d
def p_in2(p):
    """in2 : expression IN '(' positive_unary_tests ')'"""
    p[0] = AST.In(p[1], p[4])


# 52
def p_filter_expression(p):
    """filter_expression : expression '[' expression ']'"""
    p[0] = AST.FilterExpression(p[1], p[3])


# 53
def p_instance_of(p):
    """instance_of : expression INSTANCE OF type"""
    p[0] = AST.InstanceOf(p[1], p[4])


# 54
def p_type(p):
    """type : qualified_name"""
    p[0] = AST.Type(p[1])


# 55
def p_boxes_expression(p):
    """boxes_expression : list
                        | function_definition
                        | context"""
    p[0] = p[1]


# 56
def p_list(p):
    """list : '[' positional_parameters ']'"""
    p[0] = AST.List(p[2])


# 57
def p_function_definition(p):
    """function_definition : FUNCTION '(' empty_list        ')' external expression %prec function_definition_p
                           | FUNCTION '(' formal_parameters ')' external expression %prec function_definition_p"""
    p[0] = AST.FunctionDefinition(p[3], p[5], p[6])


def p_formal_parameters(p):
    """formal_parameters : single_formal_parameter
                         | many_formal_parameters"""
    p[0] = p[1]


def p_single_formal_parameter(p):
    """single_formal_parameter : formal_parameter"""
    p[0] = [p[1]]


def p_many_formal_parameters(p):
    """many_formal_parameters : formal_parameter ',' formal_parameters"""
    p[0] = [p[1]] + p[3]


def p_external(p):
    """external : EXTERNAL
                | empty_list"""
    p[0] = p.slice[1].type == 'EXTERNAL'


# 58
def p_formal_parameter(p):
    """formal_parameter : parameter_name"""
    p[0] = p[1]


# 59
def p_context(p):
    """context : '{' context_entries '}'
               | '{' empty_list      '}'"""
    p[0] = AST.Context(p[2])


def p_context_entries(p):
    """context_entries : single_context_entry
                       | many_context_entries"""
    p[0] = p[1]


def p_single_context_entry(p):
    """single_context_entry : context_entry"""
    p[0] = [p[1]]


def p_many_context_entries(p):
    """many_context_entries : context_entry ',' context_entries"""
    p[0] = [p[1]] + p[3]


# 60
def p_context_entry(p):
    """context_entry : key ':' expression"""
    p[0] = (p[1], p[3])


# 61
def p_key(p):
    """key : name
           | STRING_LITERAL"""
    p[0] = p[1]


# 62
def p_date_time_literal(p):
    """date_time_literal : DATE          '(' STRING_LITERAL ')'
                         | TIME          '(' STRING_LITERAL ')'
                         | DATE_AND_TIME '(' STRING_LITERAL ')'
                         | DATE_AND_TIME '(' STRING_LITERAL NEWLINE ')'
                         | DURATION      '(' STRING_LITERAL ')'"""
    p[0] = create_literal(p[1], p[3])


# helper rules
def p_empty_list(p):
    """empty_list : """
    p[0] = []


def p_null(p):
    """null : NULL"""
    p[0] = AST.Null()


def p_error(p):
    if p:
        print(
            'unexpected token %s{%s} at position %s:%s' % (p.type, p.value, p.lexpos - find_first_in_lane(p), p.lineno))
        print_context(p)
    else:
        print('unexpected end of file')


parser = yacc.yacc()
simpleParser = yacc.yacc(start='simple_expression')
tableParser = yacc.yacc(start='unary_tests')
