from feel.ErrorPrinters import contextual_error, missing_token_error
from feel.lexer.Lexer import Lexer as Lexer
from feel.parser import AST
from feel.parser.common.BaseParser import BaseParser


# noinspection PyMethodMayBeStatic
class Parser(BaseParser):
    tokens = Lexer.tokens

    precedence = [
        ('right', 'function_definition_p', 'quantified_p', 'if_p', 'for_p'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', '=', 'NEQ', '<', 'LTE', '>', 'GTE', 'comparison_p'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'EXPONENT'),
        ('right', 'negation_p'),
        ('left', 'INSTANCE'),
        ('left', 'path_expression_p'),
        ('right', '.'),
        ('left', '[')
    ]

    # 1
    def p_expression(self, p):
        """expression : textual_expression
                      | boxes_expression"""
        p[0] = p[1]

    # 2
    def p_textual_expression(self, p):
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
                              | name
                              | par_textual_expression"""
        p[0] = p[1]

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

    def p_par_textual_expression(self, p):
        """par_textual_expression : '(' textual_expression ')'"""
        p[0] = p[2]

    # 18
    def p_endpoint(self, p):
        """endpoint : simple_value"""
        p[0] = AST.Endpoint(p[1])

    # 33
    def p_literal(self, p):
        """literal : simple_literal
                   | null"""
        p[0] = p[1]

    # 40
    def p_function_invocation(self, p):
        """function_invocation : expression parameters"""
        p[0] = AST.Invocation(p[1], p[2])

    # 41
    def p_parameters(self, p):
        """parameters : '(' positional_parameters ')'
                      | '(' named_parameters      ')'"""
        p[0] = p[2]

    # 42
    def p_named_parameters(self, p):
        """named_parameters : one_param_pair
                            | many_param_pairs"""
        p[0] = p[1]

    def p_one_param_pair(self, p):
        """one_param_pair : parameter_name ':' expression"""
        p[0] = [(p[1], p[3])]

    def p_many_param_pairs(self, p):
        """many_param_pairs : one_param_pair ',' named_parameters"""
        p[0] = p[1] + p[3]

    # 43
    def p_parameter_name(self, p):
        """parameter_name : name"""
        p[0] = p[1]

    # 44
    def p_positional_parameters(self, p):
        """positional_parameters : expressions
                                 | empty_list"""
        p[0] = p[1]

    def p_expressions(self, p):
        """expressions : single_expression
                       | many_expressions"""
        p[0] = p[1]

    def p_single_expression(self, p):
        """single_expression : expression"""
        p[0] = [p[1]]

    def p_many_expressions(self, p):
        """many_expressions : single_expression ',' expressions"""
        p[0] = p[1] + p[3]

    # 45
    def p_path_expression(self, p):
        """path_expression : expression '.' name"""
        p[0] = AST.Path(p[1], p[3])

    # 46
    def p_for_expression(self, p):
        """for_expression : FOR in_pairs RETURN expression %prec for_p"""
        p[0] = AST.For(p[2], p[4])

    # 47
    def p_if_expression(self, p):
        """if_expression : valid_if
                         | invalid_if_error"""
        p[0] = p[1]

    def p_valid_if(self, p):
        """valid_if : IF expression THEN expression ELSE expression %prec if_p"""
        p[0] = AST.If(p[2], p[4], p[6])

    def p_invalid_if(self, p):
        """invalid_if_error : missing_then_error
                            | missing_else_error"""
        p[0] = p[1]

    def p_missing_then_error(self, p):
        """missing_then_error : IF expression error ELSE expression"""
        missing_token_error("missing 'then' branch in 'if' expression", p[3])
        self.parser.errok()
        p[0] = AST.If(p[2], AST.Null(), p)

    def p_missing_else_error(self, p):
        """missing_else_error : IF expression THEN expression error"""
        missing_token_error("missing 'else' branch in 'if' expression", p[5])
        self.parser.errok()
        p[0] = AST.If(p[2], p[4], AST.Null())

    # 48
    def p_quantified_expression(self, p):
        """quantified_expression : SOME  in_pairs SATISFIES expression %prec quantified_p
                                 | EVERY in_pairs SATISFIES expression %prec quantified_p"""
        p[0] = AST.QuantifiedExpr(p.slice[1].type == 'SOME', p[2], p[4])

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
        p[0] = AST.Disjunction(p[1], p[3])

    # 50
    def p_conjunction(self, p):
        """conjunction : expression AND expression"""
        p[0] = AST.Conjunction(p[1], p[3])

    # 51
    def p_comparison(self, p):
        """comparison : operator
                      | between
                      | in1
                      | in2"""
        p[0] = p[1]

    # 51b
    def p_between(self, p):
        """between : between1 AND expression  %prec comparison_p"""
        expr, begin_start = p[1]
        begin_end = p[3]
        p[0] = AST.Between(expr, begin_start, begin_end)

    def p_between1(self, p):
        """between1 : expression BETWEEN expression %prec comparison_p"""
        p[0] = p[1], p[3]

    # 51c
    def p_in1(self, p):
        """in1 : expression IN positive_unary_test %prec comparison_p"""
        p[0] = AST.In(p[1], AST.PositiveUnaryTests([p[3]]))

    # 51d
    def p_in2(self, p):
        """in2 : expression IN '(' positive_unary_tests ')' %prec comparison_p"""
        p[0] = AST.In(p[1], p[4])

    # 52
    def p_filter_expression(self, p):
        """filter_expression : expression '[' expression ']'"""
        p[0] = AST.FilterExpression(p[1], p[3])

    # 53
    def p_instance_of(self, p):
        """instance_of : expression INSTANCE OF type"""
        p[0] = AST.InstanceOf(p[1], p[4])

    # 54
    def p_type(self, p):
        """type : qualified_name"""
        p[0] = AST.Type(p[1])

    # 55
    def p_boxes_expression(self, p):
        """boxes_expression : list
                            | function_definition
                            | context"""
        p[0] = p[1]

    # 56
    def p_list(self, p):
        """list : '[' positional_parameters ']'"""
        p[0] = AST.List(p[2])

    # 57
    def p_function_definition(self, p):
        """function_definition : FUNCTION '(' empty_list        ')' external expression %prec function_definition_p
                               | FUNCTION '(' formal_parameters ')' external expression %prec function_definition_p"""
        p[0] = AST.FunctionDefinition(p[3], p[5], p[6])

    def p_formal_parameters(self, p):
        """formal_parameters : single_formal_parameter
                             | many_formal_parameters"""
        p[0] = p[1]

    def p_single_formal_parameter(self, p):
        """single_formal_parameter : formal_parameter"""
        p[0] = [p[1]]

    def p_many_formal_parameters(self, p):
        """many_formal_parameters : formal_parameter ',' formal_parameters"""
        p[0] = [p[1]] + p[3]

    def p_external(self, p):
        """external : EXTERNAL
                    | empty_list"""
        p[0] = p.slice[1].type == 'EXTERNAL'

    # 58
    def p_formal_parameter(self, p):
        """formal_parameter : parameter_name"""
        p[0] = p[1]

    # 59
    def p_context(self, p):
        """context : '{' context_entries '}'
                   | '{' empty_list      '}'"""
        p[0] = AST.Context(p[2])

    def p_context_entries(self, p):
        """context_entries : single_context_entry
                           | many_context_entries
                           | missing_comma_error"""
        p[0] = p[1]

    def p_single_context_entry(self, p):
        """single_context_entry : context_entry"""
        p[0] = [p[1]]

    def p_many_context_entries(self, p):
        """many_context_entries : context_entry ',' context_entries"""
        p[0] = [p[1]] + p[3]

    def p_missing_comma_error(self, p):
        """missing_comma_error : context_entry ',' error"""
        missing_token_error('comma is missing in a context', p[3])
        self.parser.errok()
        p[0] = []

    # 60
    def p_context_entry(self, p):
        """context_entry : key ':' expression"""
        p[0] = (p[1], p[3])

    # 61
    def p_key(self, p):
        """key : name
               | STRING_LITERAL"""
        p[0] = p[1]

    def p_null(self, p):
        """null : NULL"""
        p[0] = AST.Null()

    def __init__(self, **kwargs) -> None:
        super(Parser, self).__init__(**kwargs)
        self.lexer = Lexer()


parser = Parser()
