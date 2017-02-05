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
        ('left',  'OR'),
        #        | conjunction |
        ('left',  'AND'),
        #        | comparison a) |
        ('left',  'EQ', 'NEQ', 'LT', 'LTE', 'GT', 'GTE'),
        #        | comparison b) |
        ('left',  'BETWEEN'),
        #        | comparison c) |
        ('left',  'IN'),
        #        | instance of |
        ('left',  'INSTANCE'),
        ('right', '.'),
        #        | filter expressions |
        ('right', '['),
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
                              | instance_of
                              | path_expression
                              | filter_expression
                              | function_invocation
                              | literal
                              | NAME"""
        p[0] = TextualExpression(p[1])

    # 15
    def p_positive_unary_test(self, p):
        """positive_unary_test : NULL"""
        p[0] = Null()

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

    # 20
    def p_qualified_name(self, p):
        """qualified_name : NAME names"""
        p[0] = [p[1]] + p[2]

    def p_names(self, p):
        """names : dot_names
                 | empty"""
        p[0] = p[1]

    def p_dot_names(self, p):
        """dot_names :  '.' qualified_name"""
        p[0] = p[2]

    # 33
    def p_literal(self, p):
        """literal : simple_literal"""
        p[0] = Literal(p[1])

    # 34
    def p_simple_literal(self, p):
        """simple_literal : STRING_LITERAL
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
        """parameter_name : NAME"""
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
        """path_expression : expression '.' NAME"""
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
        """one_in_pair : NAME IN expression"""
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
        """list : '[' list_expressions ']'"""
        p[0] = p[2]

    def p_list_expressions(self, p):
        """list_expressions : many_expressions
                            | list_expression
                            | empty"""
        p[0] = p[1]

    def p_many_expressions(self, p):
        """many_expressions : list_expressions ',' list_expression"""
        p[0] = p[1] + p[3]

    def p_list_expression(self, p):
        """list_expression : expression"""
        p[0] = [p[1]]

    # 57
    def p_function_definition(self, p):
        """function_definition : FUNCTION '(' formal_parameters ')' function_type expression"""
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
                             | formal_parameter
                             | empty"""
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
        """context : '{' context_entries '}'"""
        p[0] = Context(p[2])

    def p_context_entries(self, p):
        """context_entries : many_entries
                           | one_entry
                           | zero_entries"""
        p[0] = p[1]

    def p_many_entries(self, p):
        """many_entries : one_entry ',' context_entries"""
        p[0] = p[1] + p[3]

    def p_one_entry(self, p):
        """one_entry : context_entry"""
        p[0] = [p[1]]

    def p_zero_entries(self, p):
        """zero_entries : empty"""
        p[0] = []

    # 60
    def p_context_entry(self, p):
        """context_entry : key ':' expression"""
        p[0] = ContextEntry(p[1], p[3])

    # 61
    def p_key(self, p):
        """key : NAME
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
        print 'Ill tok: %s' % p

    def parse(self, *args, **kwargs):
        return self.parser.parse(lexer=lexer, *args, **kwargs)

# parser = yacc.yacc()
