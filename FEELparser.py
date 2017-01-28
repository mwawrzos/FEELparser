from ply import yacc
from FEEL_AST import *
from FEELlexer import tokens, lexer


def create_literal(literal, *args):
    name = literal.title().replace(' ', '_') + "Literal"
    return globals()[name](*args)


class FeelParser:
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
                              | literal
                              | NAME"""
        p[0] = TextualExpression(p[1])

# 20
#     def p_qualified_name(self, p):
#         """qualified_name : names"""
#         p[0] = p[1]
#
    # def p_names(self, p):
    #     """names : many_names
    #              | one_name
    #              | empty"""
    #     p[0] = p[1]
    #
    # def p_many_names(self, p):
    #     """many_names : one_name ',' names"""
    #     p[0] = p[1] + [p[3]]
    #
    # def p_one_name(self, p):
    #     """one_name : NAME"""
    #     p[0] = [p[1]]

# 33
    def p_literal(self, p):
        """literal : simple_literal"""
        p[0] = Literal(p[1])

# 34
    def p_simple_literal(self, p):
        """simple_literal : STRING_LITERAL
                          | date_time_literal"""
        p[0] = SimpleLiteral(p[1])

# 43
    def p_parameter_name(self, p):
        """parameter_name : NAME"""
        p[0] = p[1]

# 53
#     def p_instance_of(self, p):
#         """instance_of : expression INSTANCE OF type"""
#         p[0] = InstanceOf(p[1], p[4])

    # def p_instanced_expression(self, p):
    #     """expression2 : expression"""

# 54
#     def p_type(self, p):
#         """type : qualified_name"""
#         p[0] = p[1]

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

    def p_error(self, p):
        print 'Ill tok: %s'% p

    def parse(self, *args, **kwargs):
        return self.parser.parse(lexer=lexer, *args, **kwargs)

    def p_empty(self, p):
        """empty : """
        p[0] = []

# parser = yacc.yacc()
