import unittest

from FEEL_AST import *
from FEELparser import FeelParser
from FEELlexer import lexer

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

FUNCTION_A_EXPRESSION = Expression(TextualExpression(FunctionDefinition([], DATE_EXPRESSION)))
FUNCTION_B_EXPRESSION = Expression(TextualExpression(ExternalFunctionDefinition(['x', 'y', 'z'],
                                                                                CAT_CONTEXT_EXPRESSION)))

EMPTY_LIST_EXPRESSION = Expression(BoxedExpression([]))
LIST_EXPRESSION = Expression(BoxedExpression([FUNCTION_B_EXPRESSION,
                                              CAT_CONTEXT_EXPRESSION,
                                              DATE_EXPRESSION]))

IZA_INSTANCE_EXPRESSION = Expression(TextualExpression(InstanceOf(LIST_EXPRESSION, ['Iza'])))
ALA_INSTANCE_EXPRESSION = Expression(TextualExpression(InstanceOf(FUNCTION_B_EXPRESSION, ['Ala', 'ma', 'kota'])))

CAT_CONTEXT_STR = '{cat:date(""),"cat":time("")}'
FUNCTION_B_STR = 'function(x,y,z) external ' + CAT_CONTEXT_STR
LIST_STR = '[' + FUNCTION_B_STR + ',' + CAT_CONTEXT_STR + ', date("")]'


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
        self.check_parser('function()date("")', FUNCTION_A_EXPRESSION)
        self.check_parser(FUNCTION_B_STR, FUNCTION_B_EXPRESSION)

    def test_list_is_expression(self):
        self.check_parser('[]', EMPTY_LIST_EXPRESSION)
        self.check_parser(LIST_STR, LIST_EXPRESSION)

    # def test_instance_of_is_expression(self):
    #     self.check_parser(LIST_STR + ' instance of Iza',
    #                       IZA_INSTANCE_EXPRESSION)
    #     self.check_parser(FUNCTION_B_STR + ' instance of Ala, ma, kota',
    #                       ALA_INSTANCE_EXPRESSION)

    def test_name_is_expression(self):
        self.check_parser('name', NAME_EXPRESSION)

    def check_parser(self, code, expression):
        self.assertEqual(self.parser.parse(
            code),
            expression)


if __name__ == '__main__':
    unittest.main()
