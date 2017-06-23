from ply import yacc
from FEEL_AST import *
from FEELlexer import tokens, lexer


def create_literal(literal, *args):
    name = literal.title().replace(' ', '_') + "Literal"
    return globals()[name](*args)


class FeelParser:
    precedence = (
        #        |   functions   |   for   |   if  | quantified |
        ('right', ')', 'EXTERNAL', 'RETURN', 'ELSE', 'SATISFIES'),
        #        | disjunction |
        ('left', 'OR'),
        #        | conjunction |
        ('left', 'AND'),
        #        | comparison a) |
        ('left', 'EQ', 'NEQ', 'LT', 'LTE', 'GT', 'GTE'),
        #        | comparison b) |
        ('left', 'BETWEEN'),
        #        | comparison c) |
        ('left', '-', '+'),
        #        | arithmetic a) |
        ('left', '/', '*'),
        #        | arithmetic b) |
        ('left', 'EXPONENT'),
        #        | arithmetic c) |
        ('left', 'IN'),
        #        | instance of |
        ('left', 'INSTANCE'),
        #        | filter expressions |
        ('right', '['),
        ('left', ']'),
        ('right', '.'),
        ('right', '(')
    )

    def __init__(self, **kwargs):
        self.tokens = tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    # 1
    def p_expression(self, p):
        """expression : textual_expression
                      | boxed_expression"""
        p[0] = Expression(p[1])

    # 2
    def p_textual_expression(self, p):
        """textual_expression : function_definition
                              | for_expression
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
                              | simple_positive_unary_test
                              | name
                              | par_expression"""
        p[0] = TextualExpression(p[1])

    def p_par_expression(self, p):
        """par_expression : '(' textual_expression ')'"""
        p[0] = p[2]

    # 4
    def p_arithmetic_expression(self, p):
        """arithmetic_expression : addition
                                 | subtraction
                                 | multiplication
                                 | division
                                 | exponentiation
                                 | arithmetic_negation"""
        p[0] = ArithmeticExpression(p[1])

    # 7
    def p_simple_positive_unary_test(self, p):
        """simple_positive_unary_test : interval
                                      | unary_comparison"""
        p[0] = SimplePositiveUnaryTest(p[1])

    def p_unary_comparison(self, p):
        """unary_comparison : LT  endpoint
                            | LTE endpoint
                            | GT  endpoint
                            | GTE endpoint"""
        p[0] = p[1](None, p[2])

    # 8
    def p_interval(self, p):
        """interval : interval1 DOTS interval2"""
        p[0] = p[3](p[1])

    def p_interval1(self, p):
        """interval1 : open_interval_start
                     | closed_interval_start"""
        p[0] = p[1]

    def p_interval2(self, p):
        """interval2 : open_interval_end
                     | closed_interval_end"""
        p[0] = p[1]

    # def p_interval_start(self, p):
    #     """interval_start : open_interval_start
    #                       | closed_interval_start"""
    #     p[0] = p[1]

    # def p_interval_end(self, p):
    #     """interval_end : open_interval_end
    #                     | closed_interval_end"""
    #     p[0] = p[1]

    # 9
    def p_open_interval_start(self, p):
        """open_interval_start : '(' endpoint
                               | ']' endpoint"""
        e1 = p[2]
        p[0] = lambda e2, end: Interval(OpenIntervalStart(), e1, e2, end)

    def p_closed_interval_start(self, p):
        """closed_interval_start : '[' endpoint"""
        e1 = p[2]
        p[0] = lambda e2, end: Interval(ClosedIntervalStart(), e1, e2, end)

    # 11
    def p_open_interval_end(self, p):
        """open_interval_end : endpoint ')'
                             | endpoint '['"""
        e2 = p[1]
        p[0] = lambda foo: foo(e2, OpenIntervalEnd())

    # 12
    def p_closed_interval_end(self, p):
        """closed_interval_end : endpoint ']'"""
        e2 = p[1]
        p[0] = lambda foo: foo(e2, ClosedIntervalEnd())

    # 15
    def p_positive_unary_test(self, p):
        """positive_unary_test : NULL"""
        p[0] = p[1]

    # 16
    def p_positive_unary_tests(self, p):
        """positive_unary_tests : one_positive_unary_test
                                | many_positive_unary_tests"""
        p[0] = p[1]

    def p_one_positive_unary_test(self, p):
        """one_positive_unary_test : positive_unary_test"""
        p[0] = [p[1]]

    def p_many_positive_unary_tests(self, p):
        """many_positive_unary_tests : one_positive_unary_test ',' positive_unary_tests"""
        p[0] = p[1] + p[3]

    # 18
    def p_endpoint(self, p):
        """endpoint : simple_value"""
        p[0] = p[1]

    # 19
    def p_simple_value(self, p):
        """simple_value : qualified_name
                        | simple_literal"""
        p[0] = p[1]

    # 20
    def p_qualified_name(self, p):
        """qualified_name : names"""
        p[0] = p[1]  # + [p[2]]

    def p_names(self, p):
        """names : name '.'   qualified_name
                 | name empty empty"""
        p[0] = [p[1]] + p[3]

    # def p_dot_names(self, p):
    #     """dot_names : qualified_name '.'"""
    #     p[0] = p[1]
    #
    # 21
    def p_addition(self, p):
        """addition : expression '+' expression"""
        p[0] = Addition(p[1], p[3])

    # 22
    def p_subtraction(self, p):
        """subtraction : expression '-' expression"""
        p[0] = Subtraction(p[1], p[3])

    # 23
    def p_multiplication(self, p):
        """multiplication : expression '*' expression"""
        p[0] = Multiplication(p[1], p[3])

    # 24
    def p_division(self, p):
        """division : expression '/' expression"""
        p[0] = Division(p[1], p[3])

    # 25
    def p_exponentiation(self, p):
        """exponentiation : expression EXPONENT expression"""
        p[0] = Exponentiation(p[1], p[3])

    # 26
    def p_arithmetic_negation(self, p):
        """arithmetic_negation : '-' expression"""
        p[0] = ArithmeticNegation(p[2])

    # 27
    def p_name(self, p):
        """name : NAME"""
        p[0] = Name(p[1])

    # 33
    def p_literal(self, p):
        """literal : simple_literal
                   | NULL"""
        p[0] = Literal(p[1])

    # 34
    def p_simple_literal(self, p):
        """simple_literal : NUMERIC_LITERAL
                          | STRING_LITERAL
                          | BOOLEAN_LITERAL
                          | date_time_literal"""
        p[0] = SimpleLiteral(p[1])

    # 40
    def p_function_invocation(self, p):
        """function_invocation : expression parameters"""
        p[0] = FunctionInvocation(p[1], p[2])

    # 41
    def p_parameters(self, p):
        """parameters : '(' positional_parameters ')'
                      | '(' named_parameters      ')'"""
        p[0] = p[2]

    # 42
    def p_named_parameters(self, p):
        """named_parameters : named_parameters1"""
        p[0] = NamedParameters(p[1])

    def p_named_parameters1(self, p):
        """named_parameters1 : one_named_parameter
                             | many_named_parameters"""
        p[0] = p[1]

    def p_one_named_parameter(self, p):
        """one_named_parameter : parameter_name ':' expression"""
        p[0] = [(p[1], p[3])]

    def p_many_named_parameters(self, p):
        """many_named_parameters : one_named_parameter ',' named_parameters1"""
        p[0] = p[1] + p[3]

    # 43
    def p_parameter_name(self, p):
        """parameter_name : name"""
        p[0] = p[1]

    # 44
    def p_positional_parameters(self, p):
        """positional_parameters : positional_parameters1
                                 | empty"""
        p[0] = PositionalParameters(p[1])

    def p_positional_parameters1(self, p):
        """positional_parameters1 : one_positional_parameter
                                  | many_positional_parameters"""
        p[0] = p[1]

    def p_one_positional_parameter(self, p):
        """one_positional_parameter : expression"""
        p[0] = [p[1]]

    def p_many_positional_parameters(self, p):
        """many_positional_parameters : one_positional_parameter ',' positional_parameters1"""
        p[0] = p[1] + p[3]

    # 45
    def p_path_expression(self, p):
        """path_expression : expression '.' name"""
        p[0] = PathExpression(p[1], p[3])

    # 46
    def p_for_expression(self, p):
        """for_expression : FOR in_pairs RETURN expression"""
        p[0] = ForExpression(p[2], p[4])

    # 47
    def p_if_expression(self, p):
        """if_expression : IF expression THEN expression ELSE expression"""
        p[0] = IfExpression(p[2], p[4], p[6])

    # 48
    def p_quantified_expression(self, p):
        """quantified_expression : SOME  in_pairs SATISFIES expression
                                 | EVERY in_pairs SATISFIES expression"""
        p[0] = p[1](p[2], p[4])

    def p_in_pairs(self, p):
        """in_pairs : one_in_pair
                    | many_in_pairs"""
        p[0] = p[1]

    def p_one_in_pair(self, p):
        """one_in_pair : name IN expression"""
        p[0] = [(p[1], p[3])]

    def p_many_in_pairs(self, p):
        """many_in_pairs : one_in_pair in_pairs"""
        p[0] = p[1] + p[2]

    # 49
    def p_disjunction(self, p):
        """disjunction : expression OR expression"""
        p[0] = Disjunction(p[1], p[3])

    # 50
    def p_conjunction(self, p):
        """conjunction : expression AND expression"""
        p[0] = Conjunction(p[1], p[3])

    # 51
    def p_comparison(self, p):
        """comparison : logical
                      | between
                      | in1
                      | in2"""
        p[0] = Comparison(p[1])

    # a
    def p_logical(self, p):
        """logical : expression EQ  expression
                   | expression NEQ expression
                   | expression LT  expression
                   | expression LTE expression
                   | expression GT  expression
                   | expression GTE expression"""
        p[0] = p[2](p[1], p[3])

    # b
    def p_between(self, p):
        """between : between1 AND expression"""
        p[0] = p[1](p[3])

    def p_between1(self, p):
        """between1 : expression BETWEEN expression"""
        expression = p[1]
        lower_bound = p[3]
        p[0] = lambda upper_bound: Between(expression, lower_bound, upper_bound)

    # c
    def p_in1(self, p):
        """in1 : expression IN positive_unary_test"""
        p[0] = In(p[1], [p[3]])

    # d
    def p_in2(self, p):
        """in2 : expression IN '(' positive_unary_tests ')'"""
        p[0] = In(p[1], p[4])

    # 52
    def p_filter_expression(self, p):
        """filter_expression : expression '[' expression ']'"""
        p[0] = FilterExpression(p[1], p[3])

    # 53
    def p_instance_of(self, p):
        """instance_of : expression INSTANCE OF type"""
        p[0] = InstanceOf(p[1], p[4])

    # 54
    def p_type(self, p):
        """type : qualified_name"""
        p[0] = p[1]

    # 55
    def p_boxed_expression(self, p):
        """boxed_expression : list
                            | context"""
        p[0] = BoxedExpression(p[1])

    # 56
    def p_list(self, p):
        """list : list1
                | list2"""
        p[0] = p[1]

    def p_list1(self, p):
        """list1 : '[' list_expressions ']'"""
        p[0] = p[2]

    def p_list2(self, p):
        """list2 : '[' ']'"""
        p[0] = []

    def p_list_expressions(self, p):
        """list_expressions : many_expressions
                            | list_expression"""
        p[0] = p[1]

    def p_many_expressions(self, p):
        """many_expressions : list_expressions ',' list_expression"""
        p[0] = p[1] + p[3]

    def p_list_expression(self, p):
        """list_expression : expression"""
        p[0] = [p[1]]

    # 57
    def p_function_definition(self, p):
        """function_definition : FUNCTION '(' formal_parameters ')' function_type expression
                               | FUNCTION '('       empty       ')' function_type expression"""
        p[0] = p[5](p[3], p[6])

    def p_function_type(self, p):
        """function_type : external_function
                         | non_external_function"""
        p[0] = p[1]

    def p_external_function(self, p):
        """external_function : EXTERNAL"""
        p[0] = ExternalFunctionDefinition

    def p_non_external_function(self, p):
        """non_external_function : empty"""
        p[0] = FunctionDefinition

    def p_formal_parameters(self, p):
        """formal_parameters : many_parameters
                             | formal_parameter"""
        p[0] = p[1]

    def p_many_parameters(self, p):
        """many_parameters : formal_parameter ',' formal_parameters"""
        p[0] = p[1] + p[3]

    # 58
    def p_formal_parameter(self, p):
        """formal_parameter : parameter_name"""
        p[0] = [p[1]]

    # 59
    def p_context(self, p):
        """context : '{' context_entries '}'
                   | '{'      empty      '}'"""
        p[0] = Context(p[2])

    def p_context_entries(self, p):
        """context_entries : many_entries
                           | one_entry"""
        p[0] = p[1]

    def p_many_entries(self, p):
        """many_entries : one_entry ',' context_entries"""
        p[0] = p[1] + p[3]

    def p_one_entry(self, p):
        """one_entry : context_entry"""
        p[0] = [p[1]]

    # 60
    def p_context_entry(self, p):
        """context_entry : key ':' expression"""
        p[0] = ContextEntry(p[1], p[3])

    # 61
    def p_key(self, p):
        """key : name
               | STRING_LITERAL"""
        p[0] = Key(p[1])

    # 62
    def p_date_time_literal(self, p):
        """date_time_literal : DATE          '(' STRING_LITERAL ')'
                             | TIME          '(' STRING_LITERAL ')'
                             | date_and_time '(' STRING_LITERAL ')'
                             | DURATION      '(' STRING_LITERAL ')'"""
        p[0] = create_literal(p[1], p[3])

    def p_date_and_time(self, p):
        """date_and_time : DATE AND TIME"""
        p[0] = "date and time"

    def p_empty(self, p):
        """empty : """
        p[0] = []

    def p_error(self, p):
        print('Ill tok: %s' % p)

    def parse(self, *args, **kwargs):
        return self.parser.parse(lexer=lexer, *args, **kwargs)

# parser = yacc.yacc()
