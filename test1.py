import unittest

from FEEL_AST import *
from FEELparser import FeelParser
from FEELlexer import lexer


def function_definition(ALA_INSTANCE):
    return Expression(TextualExpression(FunctionDefinition([], ALA_INSTANCE)))


STRING_LITERAL = '""'

STRING_EXPRESSION = Expression(TextualExpression(Literal(SimpleLiteral(STRING_LITERAL))))
DATE = DateLiteral(STRING_LITERAL)
TIME = TimeLiteral(STRING_LITERAL)
DATE_AND_TIME = Date_And_TimeLiteral(STRING_LITERAL)
DURATION = DurationLiteral(STRING_LITERAL)
DATE_EXPRESSION = Expression(TextualExpression(Literal(SimpleLiteral(DATE))))
TIME_EXPRESSION = Expression(TextualExpression(Literal(SimpleLiteral(TIME))))
DATE_AND_TIME_EXPRESSION = Expression(TextualExpression(Literal(SimpleLiteral(DATE_AND_TIME))))
DURATION_EXPRESSION = Expression(TextualExpression(Literal(SimpleLiteral(DURATION))))
NAME_EXPRESSION = Expression(TextualExpression("name"))
EMPTY_CONTEXT_EXPRESSION = Expression(BoxedExpression(Context([])))
NAME_KEY = Key('cat')
STRING_KEY = Key('"cat"')
NAME_CAT = ContextEntry(NAME_KEY, DATE_EXPRESSION)
STR_CAT = ContextEntry(STRING_KEY, TIME_EXPRESSION)

CAT_CONTEXT_EXPRESSION = Expression(BoxedExpression(Context([NAME_CAT, STR_CAT])))
FUNCTION_A_EXPRESSION = function_definition(DATE_EXPRESSION)

FUNCTION_B_EXPRESSION = Expression(TextualExpression(ExternalFunctionDefinition(['x', 'y', 'z'],
                                                                                CAT_CONTEXT_EXPRESSION)))
EMPTY_LIST_EXPRESSION = Expression(BoxedExpression([]))

LIST_EXPRESSION = Expression(BoxedExpression([FUNCTION_B_EXPRESSION,
                                              CAT_CONTEXT_EXPRESSION,
                                              DATE_EXPRESSION]))
IZA_INSTANCE_EXPRESSION = Expression(TextualExpression(InstanceOf(LIST_EXPRESSION, ['Iza'])))
ALA_INSTANCE = Expression(TextualExpression(InstanceOf(DATE_EXPRESSION, ['Ala', 'ma', 'kota'])))

ALA_INSTANCE_EXPRESSION = function_definition(ALA_INSTANCE)

FILTER_EXPRESSION = Expression(TextualExpression(FilterExpression(IZA_INSTANCE_EXPRESSION,
                                                                  ALA_INSTANCE_EXPRESSION)))

BETWEEN_EXPRESSION = function_definition(Expression(TextualExpression(Comparison(Between(DATE_EXPRESSION,
                                                                                         STRING_EXPRESSION,
                                                                                         DATE_EXPRESSION)))))

IN_A_EXPRESSION = function_definition(Expression(TextualExpression(Comparison(In(DATE_EXPRESSION, [Null()])))))

IN_B_EXPRESSION = function_definition(Expression(TextualExpression(Comparison(In(DATE_EXPRESSION, [Null(), Null()])))))

CONJUNCTION_EXPRESSION = Expression(TextualExpression(Conjunction(STRING_EXPRESSION, NAME_EXPRESSION)))


def COMPARISON(operator):
    return Expression(TextualExpression(Comparison(operator(DATE_EXPRESSION, STRING_EXPRESSION))))


def LOGICAL_CMP_EXPRESSION(operator):
    return Expression(TextualExpression(FunctionDefinition([], COMPARISON(operator))))


CAT_CONTEXT_STR = '{cat:date(""),"cat":time("")}'
FUNCTION_A_STR = 'function()date("")'
FUNCTION_B_STR = 'function(x,y,z) external %s' % CAT_CONTEXT_STR
LIST_STR = '[%s, %s, %s]' % (FUNCTION_B_STR, CAT_CONTEXT_STR, 'date("")')
IZA_STR = '%s instance of Iza' % LIST_STR
ALA_STR = '%s instance of Ala. ma.kota' % FUNCTION_A_STR
FILTER_STR = '%s[%s]' % (IZA_STR, ALA_STR)


def debug_lex(expr):
    lexer.input(expr)
    for t in lexer:
        print t


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.parser = FeelParser()

    def test_date_time_literal_is_expression(self):
        self.check_parser('date("")', DATE_EXPRESSION)
        self.check_parser('time("")', TIME_EXPRESSION)
        self.check_parser('date and time("")', DATE_AND_TIME_EXPRESSION)
        self.check_parser('duration("")', DURATION_EXPRESSION)

    def test_context_is_expression(self):
        self.check_parser('{}', EMPTY_CONTEXT_EXPRESSION)
        self.check_parser(CAT_CONTEXT_STR, CAT_CONTEXT_EXPRESSION)

    def test_function_definition_is_expression(self):
        self.check_parser(FUNCTION_A_STR, FUNCTION_A_EXPRESSION)
        self.check_parser(FUNCTION_B_STR, FUNCTION_B_EXPRESSION)

    def test_list_is_expression(self):
        self.check_parser('[]', EMPTY_LIST_EXPRESSION)
        self.check_parser(LIST_STR, LIST_EXPRESSION)

    def test_instance_of_is_expression(self):
        self.check_parser(IZA_STR, IZA_INSTANCE_EXPRESSION)
        self.check_parser(ALA_STR, ALA_INSTANCE_EXPRESSION)

    def test_filter_expression_is_expression(self):
        self.check_parser(FILTER_STR, FILTER_EXPRESSION)

    def test_comparison_is_expression(self):
        self.check_operator('=', Eq)
        self.check_operator('!=', Neq)
        self.check_operator('<', Lt)
        self.check_operator('<=', Lte)
        self.check_operator('>', Gt)
        self.check_operator('>=', Gte)

        self.check_parser('%s between %s and %s' % (FUNCTION_A_STR, STRING_LITERAL, 'date("")'),
                          BETWEEN_EXPRESSION)

        self.check_parser('%s in null' % FUNCTION_A_STR, IN_A_EXPRESSION)

        self.check_parser('%s in (null, null)' % FUNCTION_A_STR,
                          IN_B_EXPRESSION)

    # def test_conjunction_is_expression(self):
    #     self.check_parser('%s and %s' % (STRING_LITERAL, 'name'),
    #                       CONJUNCTION_EXPRESSION)

    def test_name_is_expression(self):
        self.check_parser('name', NAME_EXPRESSION)

    def check_parser(self, code, expression):
        self.assertEqual(self.parser.parse(
            code),
            expression)

    def check_operator(self, operator, operator_ast):
        self.check_parser('%s %s %s' % (FUNCTION_A_STR, operator, STRING_LITERAL),
                          LOGICAL_CMP_EXPRESSION(operator_ast))


if __name__ == '__main__':
    unittest.main()
