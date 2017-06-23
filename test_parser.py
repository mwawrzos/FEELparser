import unittest

from FEEL_AST import *
from FEELparser import FeelParser
from FEELlexer import lexer


def function_definition(expression):
    return Expression(TextualExpression(FunctionDefinition([], expression)))


def txt_expr(expression):
    return Expression(TextualExpression(expression))


def arithmetic_expression(expression):
    return txt_expr(ArithmeticExpression(expression))


def simple_literal(literal):
    return txt_expr(Literal(SimpleLiteral(literal)))


STRING_LITERAL = '""'

STRING_EXPRESSION = txt_expr(Literal(SimpleLiteral('')))
DATE = DateLiteral('')
TIME = TimeLiteral('')
DATE_AND_TIME = Date_And_TimeLiteral('')
DURATION = DurationLiteral('')
DATE_EXPRESSION = txt_expr(Literal(SimpleLiteral(DATE)))
TIME_EXPRESSION = txt_expr(Literal(SimpleLiteral(TIME)))
DATE_AND_TIME_EXPRESSION = txt_expr(Literal(SimpleLiteral(DATE_AND_TIME)))
DURATION_EXPRESSION = txt_expr(Literal(SimpleLiteral(DURATION)))
NAME_EXPRESSION = txt_expr(Name('name'))
EMPTY_CONTEXT_EXPRESSION = Expression(BoxedExpression(Context([])))
NAME_KEY = Key(Name('cat'))
STRING_KEY = Key('cat')
NAME_CAT = ContextEntry(NAME_KEY, DATE_EXPRESSION)
STR_CAT = ContextEntry(STRING_KEY, TIME_EXPRESSION)

CAT_CONTEXT_EXPRESSION = Expression(BoxedExpression(Context([NAME_CAT, STR_CAT])))
FUNCTION_A_EXPRESSION = function_definition(DATE_EXPRESSION)

FUNCTION_B_EXPRESSION = txt_expr(ExternalFunctionDefinition([Name('x'), Name('y'), Name('z')],
                                                            CAT_CONTEXT_EXPRESSION))
EMPTY_LIST_EXPRESSION = Expression(BoxedExpression([]))

LIST_EXPRESSION = Expression(BoxedExpression([FUNCTION_B_EXPRESSION,
                                              CAT_CONTEXT_EXPRESSION,
                                              DATE_EXPRESSION]))
IZA_INSTANCE_EXPRESSION = txt_expr(InstanceOf(LIST_EXPRESSION, [Name('Iza')]))
QUALIFIED_ALA = [Name('Ala'), Name('ma'), Name('kota')]
ALA_INSTANCE = txt_expr(InstanceOf(DATE_EXPRESSION, QUALIFIED_ALA))

ALA_INSTANCE_EXPRESSION = function_definition(ALA_INSTANCE)

FILTER_EXPRESSION = txt_expr(FilterExpression(IZA_INSTANCE_EXPRESSION,
                                              ALA_INSTANCE_EXPRESSION))

comparison = Comparison(Between(DATE_EXPRESSION, STRING_EXPRESSION, DATE_EXPRESSION))
BETWEEN_EXPR = txt_expr(comparison)
BETWEEN_EXPRESSION = function_definition(BETWEEN_EXPR)

IN_A_EXPRESSION = function_definition(txt_expr(Comparison(In(DATE_EXPRESSION, [Null()]))))

IN_B_EXPRESSION = function_definition(txt_expr(Comparison(In(DATE_EXPRESSION, [Null(), Null()]))))

CONJUNCTION_EXPRESSION = function_definition(txt_expr(Conjunction(BETWEEN_EXPR,
                                                                  NAME_EXPRESSION)))

DISJUNCTION_EXPRESSION = function_definition(txt_expr(Disjunction(BETWEEN_EXPR,
                                                                  NAME_EXPRESSION)))

SOME_EXPRESSION = txt_expr(SomeQuantifiedExpression([(Name('name'), STRING_EXPRESSION)], STRING_EXPRESSION))
NAME_PAIRS = [(Name('name'), STRING_EXPRESSION), (Name('name'), STRING_EXPRESSION)]
EVERY_EXPRESSION = txt_expr(
    EveryQuantifiedExpression(NAME_PAIRS, STRING_EXPRESSION))

IF_EXPRESSION = txt_expr(IfExpression(STRING_EXPRESSION, STRING_EXPRESSION, STRING_EXPRESSION))

FOR_EXPRESSION = txt_expr(ForExpression(NAME_PAIRS, STRING_EXPRESSION))

PATH_EXPRESSION = txt_expr(PathExpression(STRING_EXPRESSION, Name('name')))

EMPTY_CALL_EXPRESSION = txt_expr(FunctionInvocation(STRING_EXPRESSION,
                                                    PositionalParameters([])))

POSITIONAL_CALL_EXPRESSION = txt_expr(FunctionInvocation(STRING_EXPRESSION,
                                                         PositionalParameters([STRING_EXPRESSION] * 3)))
NAMED_CALL_EXPRESSION = txt_expr(FunctionInvocation(STRING_EXPRESSION,
                                                    NamedParameters([(Name('name'), STRING_EXPRESSION)] * 3)))

TWO = simple_literal(2)


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
BETWEEN_STR = '%s between %s and %s' % (FUNCTION_A_STR, STRING_LITERAL, 'date("")')


def debug_lex(expr):
    lexer.input(expr)
    for t in lexer:
        print(t)


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.parser = FeelParser()

    def check_parser(self, code, expression):
        self.assertEqual(self.parser.parse(code),
                         expression)

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
        self.check_parser('%s instance of %s' % (STRING_LITERAL, 'ala.ma.kota'),
                          txt_expr(InstanceOf(STRING_EXPRESSION, [Name('ala'), Name('ma'), Name('kota')])))
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

        self.check_parser(BETWEEN_STR,
                          BETWEEN_EXPRESSION)

        self.check_parser('%s in null' % FUNCTION_A_STR, IN_A_EXPRESSION)

        self.check_parser('%s in (null, null)' % FUNCTION_A_STR,
                          IN_B_EXPRESSION)

    def test_conjunction_is_expression(self):
        self.check_parser('%s and %s' % (BETWEEN_STR, 'name'),
                          CONJUNCTION_EXPRESSION)

    def test_disjunction_is_expression(self):
        self.check_parser('%s or %s' % (BETWEEN_STR, 'name'),
                          DISJUNCTION_EXPRESSION)

    def test_quantified_expression_is_expression(self):
        self.check_parser('some %s in %s satisfies %s' % ('name', STRING_LITERAL, STRING_LITERAL),
                          SOME_EXPRESSION)
        self.check_parser(
            'every %s in %s %s in %s satisfies %s' % ('name', STRING_LITERAL, 'name', STRING_LITERAL, STRING_LITERAL),
            EVERY_EXPRESSION)

    def test_if_expression_is_expression(self):
        self.check_parser('if %s then %s else %s' % (STRING_LITERAL, STRING_LITERAL, STRING_LITERAL),
                          IF_EXPRESSION)

    def test_for_expression_is_expression(self):
        self.check_parser(
            'for %s in %s %s in %s return %s' % ('name', STRING_LITERAL, 'name', STRING_LITERAL, STRING_LITERAL),
            FOR_EXPRESSION)

    def test_path_is_expression(self):
        self.check_parser('%s.%s' % (STRING_LITERAL, 'name'),
                          PATH_EXPRESSION)

    def test_function_invocation_is_expression(self):
        self.check_parser('%s ()' % STRING_LITERAL, EMPTY_CALL_EXPRESSION)
        self.check_parser('%s ("","","")' % STRING_LITERAL, POSITIONAL_CALL_EXPRESSION)
        self.check_parser('%s (name:"",name:"",name:"")' % STRING_LITERAL, NAMED_CALL_EXPRESSION)

    def test_numeric_literal_is_expression(self):
        self.check_parser('0', simple_literal(0))
        self.check_parser('-0', negation(simple_literal(0)))
        self.check_parser('-1', negation(simple_literal(1)))
        self.check_parser('1', simple_literal(1))
        self.check_parser('-1.4', negation(simple_literal(1.4)))
        self.check_parser('-.4', negation(simple_literal(.4)))
        self.check_parser('.4', simple_literal(.4))

    def test_boolean_literal_is_expression(self):
        self.check_parser('true', simple_literal(True))
        self.check_parser('false', simple_literal(False))

    def test_string_literal_is_expression(self):
        self.check_parser(STRING_LITERAL, STRING_EXPRESSION)
        self.check_parser('"ala"', simple_literal('ala'))

    def test_null_is_expression(self):
        self.check_parser('null', txt_expr(Literal(Null())))

    def test_name_is_expression(self):
        self.check_parser('name', NAME_EXPRESSION)

    def test_arithmetic_negation_is_expression(self):
        self.check_parser('-name', negation(NAME_EXPRESSION))

    def test_exponentiation_is_expression(self):
        self.check_parser('2**2', arithmetic_expression(Exponentiation(TWO, TWO)))

    def test_division_is_expression(self):
        self.check_parser('2/2', arithmetic_expression(Division(TWO, TWO)))

    def test_multiplication_is_expression(self):
        self.check_parser('2*2', arithmetic_expression(Multiplication(TWO, TWO)))

    def test_subtraction_is_expression(self):
        self.check_parser('2-2', arithmetic_expression(Subtraction(TWO, TWO)))

    def test_addition_is_expression(self):
        self.check_parser('2+2', arithmetic_expression(Addition(TWO, TWO)))

    def test_interval_is_expression(self):
        o_start = OpenIntervalStart()
        o_end = OpenIntervalEnd()
        c_start = ClosedIntervalStart()
        c_end = ClosedIntervalEnd()
        endpoint = SimpleLiteral(2)
        self.check_parser('(2..2]', txt_expr(SimplePositiveUnaryTest(Interval(o_start,
                                                                              endpoint,
                                                                              endpoint,
                                                                              c_end))))
        self.check_parser(']Ala.ma.kota..iza)', txt_expr(SimplePositiveUnaryTest(Interval(o_start,
                                                                                          QUALIFIED_ALA,
                                                                                          [Name('iza')],
                                                                                          o_end))))
        self.check_parser('[Ala.ma.kota..iza)', txt_expr(SimplePositiveUnaryTest(Interval(c_start,
                                                                                          QUALIFIED_ALA,
                                                                                          [Name('iza')],
                                                                                          o_end))))

    def test_simple_positive_unary_test_is_expression(self):
        endpoint = SimpleLiteral(2)
        self.check_parser('< 2', txt_expr(SimplePositiveUnaryTest(Lt(None, endpoint))))
        self.check_parser('<=2', txt_expr(SimplePositiveUnaryTest(Lte(None, endpoint))))
        self.check_parser('> 2', txt_expr(SimplePositiveUnaryTest(Gt(None, endpoint))))
        self.check_parser('>=2', txt_expr(SimplePositiveUnaryTest(Gte(None, endpoint))))

    def test_parenthesis_is_expression(self):
        two = simple_literal(2)
        some_sum = txt_expr(TextualExpression(ArithmeticExpression(Addition(two, two))))
        some_multiplication = txt_expr(ArithmeticExpression(Multiplication(some_sum, two)))
        self.check_parser('(2+2)*2', some_multiplication)
        self.check_parser('function()(2+2)*2', function_definition(some_multiplication))

    def check_operator(self, operator, operator_ast):
        self.check_parser('%s %s %s' % (FUNCTION_A_STR, operator, STRING_LITERAL),
                          LOGICAL_CMP_EXPRESSION(operator_ast))


def negation(expression):
    return arithmetic_expression(ArithmeticNegation(expression))


if __name__ == '__main__':
    unittest.main()
