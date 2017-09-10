# coding: utf8
import unittest

from feel.parser import AST
from feel.parser.parser.Parser import parser
from feel.parser.simple.SimpleParser import parser as simple_parser
from feel.parser.table.TableParser import parser as table_parser


def operator_ast_gen(operator_ast):
    return operator_ast(FILTER_EXPRESSION_AST, LIST_AST)


def operator_str_gen(operator_str):
    return '%s %s %s' % (FILTER_EXPRESSION_STR, operator_str, LIST_STR)


DATE_STR = 'date("1")'
DATE_AST = AST.Date('1')

NAME_STR = 'ala ma kota'
NAME_AST = AST.Name(NAME_STR)

CONTEXT_STR = '{%s:%s}' % (NAME_STR, DATE_STR)
CONTEXT_AST = AST.Context([(NAME_AST, DATE_AST)])

FUNCTION_STR = 'function()%s' % CONTEXT_STR
FUNCTION_AST = AST.FunctionDefinition([], False, CONTEXT_AST)

LIST_STR = '[%s, %s]' % (FUNCTION_STR, CONTEXT_STR)
LIST_AST = AST.List([FUNCTION_AST, CONTEXT_AST])

INSTANCE_OF_STR = '%s  instance  of  ala.ma.kota' % LIST_STR
# INSTANCE_OF_STR = '%s instance of ala.ma.kota' % LIST_STR
INSTANCE_OF_AST = AST.InstanceOf(LIST_AST, AST.Type([AST.Name('ala.ma.kota')]))

FILTER_EXPRESSION_STR = '%s [%s]' % (LIST_STR, INSTANCE_OF_STR)
FILTER_EXPRESSION_AST = AST.FilterExpression(LIST_AST, INSTANCE_OF_AST)

CONJUNCTION_STR = '%s and %s' % (operator_str_gen('='), INSTANCE_OF_STR)
CONJUNCTION_AST = AST.Conjunction(operator_ast_gen(AST.Eq), INSTANCE_OF_AST)

DISJUNCTION_STR = '%s  or %s' % (CONJUNCTION_STR, operator_str_gen('<='))
DISJUNCTION_AST = AST.Disjunction(CONJUNCTION_AST, operator_ast_gen(AST.Lte))

QUANTIFIED_STR = 'some  ala  in %s satisfies %s' % (DISJUNCTION_STR, CONJUNCTION_STR)
QUANTIFIED_AST = AST.QuantifiedExpr(True, [(AST.Name('ala'), DISJUNCTION_AST)], CONJUNCTION_AST)

IF_STR = 'if  %s  then %s else %s' % (QUANTIFIED_STR, DISJUNCTION_STR, CONJUNCTION_STR)
IF_AST = AST.If(QUANTIFIED_AST, DISJUNCTION_AST, CONJUNCTION_AST)

FOR_STR = 'for  ala  in  %s  return  %s' % (IF_STR, QUANTIFIED_STR)
FOR_AST = AST.For([(AST.Name('ala'), IF_AST)], QUANTIFIED_AST)

PATH_STR = '%s.ala' % DATE_STR
PATH_AST = AST.Path(DATE_AST, AST.Name('ala'))

INVOCATION_STR = '%s(%s, %s)' % (PATH_STR, FOR_STR, IF_STR)
INVOCATION_AST = AST.Invocation(PATH_AST, [FOR_AST, IF_AST])

NEGATION_STR = '-?A_zÊÝĄͼൺ⁶Ⰲ〠邏２𐎅'
NEGATION_AST = AST.Negation(AST.Name('?A_zÊÝĄͼൺ⁶Ⰲ〠邏２𐎅'))

ARITHMETIC_EXPRESSION_STR = '1.2-%s  /true  **%s' % (NEGATION_STR, NAME_STR)
ARITHMETIC_EXPRESSION_AST = AST.Dif(AST.Number(1.2), AST.Div(NEGATION_AST, AST.Exp(AST.Boolean(True), NAME_AST)))

NOT_STR = 'not (null)'
NOT_AST = AST.Not(AST.PositiveUnaryTests([AST.Null()]))

POSITIVE_UNARY_TESTS_STR = '%s  in (null, null)' % ARITHMETIC_EXPRESSION_STR
POSITIVE_UNARY_TESTS_AST = AST.In(ARITHMETIC_EXPRESSION_AST, AST.PositiveUnaryTests([AST.Null()] * 2))

POSITIVE_UNARY_TEST_STR = '%s in (null, %s)' % (POSITIVE_UNARY_TESTS_STR, DATE_STR)
POSITIVE_UNARY_TEST_AST = AST.In(POSITIVE_UNARY_TESTS_AST, AST.PositiveUnaryTests([AST.Null(), AST.Endpoint(DATE_AST)]))

SIMPLE_POSITIVE_UNARY_TESTS_STR = 'ala, "ala"'
SIMPLE_POSITIVE_UNARY_TESTS_AST = AST.PositiveUnaryTests([AST.Endpoint([AST.Name('ala')]),
                                                          AST.Endpoint(AST.StringLiteral('ala'))])


class TestParser(unittest.TestCase):
    def check_parser(self, str_input, ast, debug=False):
        self.assertEqual(ast, parser.parse(str_input, debug=debug))

    def check_simple_parser(self, str_input, ast, debug=False):
        self.assertEqual(ast, simple_parser.parse(str_input, debug=debug))

    def check_table_parser(self, str_input, ast, debug=False):
        self.assertEqual(ast, table_parser.parse(str_input, debug=debug))

    def _check_simple_unary_tests_parser(self, str_input, ast, debug=False):
        pass
        # self.assertEqual(ast, simpleUnaryTestsParser.parse(str_input, debug=debug))

    def test_date_time_literal(self):
        self.check_parser(DATE_STR, DATE_AST)
        self.check_parser('time         ("a")', AST.Time('a'))
        self.check_parser('date and time("?")', AST.DateAndTime('?'))
        self.check_parser('duration     ("#")', AST.Duration('#'))
        # self.check_parser('date  and time("")', None)

    def test_context(self):
        self.check_parser(CONTEXT_STR, CONTEXT_AST)
        self.check_parser('{{"ola":{ola_ctx}, "iza":{iza_ctx}}}'.format(ola_ctx=DATE_STR, iza_ctx=CONTEXT_STR),
                          AST.Context([('ola', DATE_AST), ('iza', CONTEXT_AST)]))

    def test_function_definition(self):
        self.check_parser(FUNCTION_STR, FUNCTION_AST)
        self.check_parser('function(ola, iza) external %s' % CONTEXT_STR,
                          AST.FunctionDefinition([AST.Name('ola'), AST.Name('iza')], True, CONTEXT_AST))
        self.check_parser('function(ola, iza) external  %s' % DATE_STR,
                          AST.FunctionDefinition([AST.Name('ola'), AST.Name('iza')], True, DATE_AST))
        # self.check_parser('function(ola, iza) external %s' % DATE_STR,
        #                   AST.FunctionDefinition(['ola', 'iza'], True, DATE_AST))

    def test_list(self):
        self.check_parser(LIST_STR, LIST_AST)
        self.check_parser('[]', AST.List([]))

    def test_instance_of(self):
        self.check_parser('%s  instance  of  a.b.c' % DATE_STR,
                          AST.InstanceOf(DATE_AST, AST.Type([AST.Name('a.b.c')])))
        # self.check_parser(INSTANCE_OF_STR,
        #                   INSTANCE_OF_AST)
        # self.check_parser('a  instance of a', AST.InstanceOf('a', 'a'))
        # self.check_parser('a instance of a', AST.InstanceOf('a', 'a'))

    def test_filter_expression(self):
        self.check_parser(FILTER_EXPRESSION_STR,
                          FILTER_EXPRESSION_AST)

    def test_comparison(self):
        self.check_operator_parser('=', AST.Eq)
        self.check_operator_parser('!=', AST.Neq)
        self.check_operator_parser('<', AST.Lt)
        self.check_operator_parser('<=', AST.Lte)
        self.check_operator_parser('>', AST.Gt)
        self.check_operator_parser('>=', AST.Gte)
        self.check_parser('%s between %s and %s' % (DATE_STR, CONTEXT_STR, LIST_STR),
                          AST.Between(DATE_AST, CONTEXT_AST, LIST_AST))
        # self.check_parser('%s between %s and %s' % (FILTER_EXPRESSION_STR, INSTANCE_OF_STR, LIST_STR),
        #                   AST.Between(FILTER_EXPRESSION_AST, INSTANCE_OF_AST, LIST_AST),
        #                   debug=True)
        self.check_parser('%s in  null' % DATE_STR,
                          AST.In(DATE_AST, AST.PositiveUnaryTests([AST.Null()])))
        self.check_parser('%s in  null' % FILTER_EXPRESSION_STR,
                          AST.In(FILTER_EXPRESSION_AST, AST.PositiveUnaryTests([AST.Null()])))
        # self.check_parser('%s in null' % FILTER_EXPRESSION_STR, AST.In(FILTER_EXPRESSION_AST, [AST.Null]))
        self.check_parser('%s in (null, null)' % FILTER_EXPRESSION_STR,
                          AST.In(FILTER_EXPRESSION_AST, AST.PositiveUnaryTests([AST.Null()] * 2)))

    def check_operator_parser(self, operator_str, operator_ast):
        self.check_parser(operator_str_gen(operator_str),
                          operator_ast_gen(operator_ast))
        self.check_parser('%s %s %s' % (FILTER_EXPRESSION_STR, operator_str, INSTANCE_OF_STR),
                          operator_ast(FILTER_EXPRESSION_AST, INSTANCE_OF_AST))

    def test_conjunction(self):
        self.check_parser(CONJUNCTION_STR,
                          CONJUNCTION_AST)
        self.check_parser('%s and  %s' % (DATE_STR, DATE_STR),
                          AST.Conjunction(DATE_AST, DATE_AST))
        # self.check_parser('%s and %s' % (DATE_STR, DATE_STR),
        #                   AST.Conjunction(DATE_AST, DATE_AST))

    def test_disjunction(self):
        self.check_parser(DISJUNCTION_STR,
                          DISJUNCTION_AST)
        # self.check_parser('%s or %s' % (CONJUNCTION_STR, operator_str_gen('<=')),
        #                   AST.Disjunction(CONJUNCTION_AST, operator_ast_gen(AST.Lte)))
        self.check_parser('%s or  %s' % (DATE_STR, DATE_STR),
                          AST.Disjunction(DATE_AST, DATE_AST))
        # self.check_parser('%s or %s' % (DATE_STR, DATE_STR),
        #                   AST.Disjunction(DATE_AST, DATE_AST))

    def test_quantified_expression(self):
        self.check_parser(QUANTIFIED_STR,
                          QUANTIFIED_AST)
        self.check_parser('every  ala  in %s satisfies %s' % (DISJUNCTION_STR, CONJUNCTION_STR),
                          AST.QuantifiedExpr(False, [(AST.Name('ala'), DISJUNCTION_AST)], CONJUNCTION_AST))
        self.check_parser('every  ala  in %s ola  in %s satisfies %s' % (DISJUNCTION_STR,
                                                                         operator_str_gen('!='),
                                                                         CONJUNCTION_STR),
                          AST.QuantifiedExpr(False,
                                             [(AST.Name('ala'), DISJUNCTION_AST),
                                              (AST.Name('ola'), operator_ast_gen(AST.Neq))],
                                             CONJUNCTION_AST))
        # self.check_parser('some ala in %s satisfies %s' % (DISJUNCTION_STR, CONJUNCTION_STR),
        #                   AST.QuantifiedExpr(True, [(AST.Name('ala'), DISJUNCTION_AST)], CONJUNCTION_AST))

    def test_if_expression(self):
        self.check_parser('if  %s then  %s else  %s' % ((DATE_STR,) * 3),
                          AST.If(*(DATE_AST,) * 3))
        self.check_parser(IF_STR,
                          IF_AST)
        # self.check_parser('if %s then %s else %s' % (QUANTIFIED_STR, DISJUNCTION_STR, CONJUNCTION_STR),
        #                   AST.If(QUANTIFIED_AST, DISJUNCTION_AST, CONJUNCTION_AST))

    def test_for_expression(self):
        self.check_parser(FOR_STR, FOR_AST)
        self.check_parser('for  ala  in  %s  ola  in  %s  return %s' % (IF_STR, QUANTIFIED_STR, DISJUNCTION_STR),
                          AST.For([(AST.Name('ala'), IF_AST), (AST.Name('ola'), QUANTIFIED_AST)],
                                  DISJUNCTION_AST))
        # self.check_parser('for ala in %s return %s' % (IF_STR, QUANTIFIED_STR),
        #                   AST.For([(AST.Name('ala'), IF_AST)], QUANTIFIED_AST))

    def test_path_expression(self):
        self.check_parser(PATH_STR, PATH_AST)

    def test_positional_parameters(self):
        self.check_parser('%s()       ' % PATH_STR,
                          AST.Invocation(PATH_AST, []))
        self.check_parser('%s(%s)    ' % (PATH_STR, FOR_STR),
                          AST.Invocation(PATH_AST, [FOR_AST]))
        self.check_parser(INVOCATION_STR, INVOCATION_AST)

    def test_named_parameters(self):
        self.check_parser('%s(ala: %s)' % (PATH_STR, INVOCATION_STR),
                          AST.Invocation(PATH_AST, [(AST.Name('ala'), INVOCATION_AST)]))
        self.check_parser('%s(ala : %s, ola :%s)' % ((DATE_STR,) * 3),
                          AST.Invocation(DATE_AST,
                                         [(AST.Name('ala'), DATE_AST), (AST.Name('ola'), DATE_AST)]))

    def test_numeric_literal(self):
        self.check_parser('1', AST.Number(1))
        self.check_parser('1.42', AST.Number(1.42))
        self.check_parser('1 . 42', AST.Number(1.42))
        self.check_parser('.42', AST.Number(.42))
        self.check_parser('. 42', AST.Number(.42))
        self.check_parser('42', AST.Number(42))
        # self.check_parser('-1', AST.Number(-1))

    def test_boolean_literal(self):
        self.check_parser('  true   ', AST.Boolean(True))
        self.check_parser('  false  ', AST.Boolean(False))

    def test_string_literal(self):
        self.check_parser('"ala"', AST.StringLiteral('ala'))

    def test_literal(self):
        self.check_parser('"ala"', AST.StringLiteral('ala'))
        self.check_parser('null', AST.Null())

    def test_additional_name_symbol(self):
        self.check_name('ala.')
        self.check_name('ala/ola')
        self.check_name('ala - ola')
        self.check_name('ala ’ola')
        self.check_name('ala+ ola')
        self.check_name('ala*-*ola')

    def test_name_part_char(self):
        self.check_name('ൺ')
        self.check_name('ൺ5')
        self.check_name('ൺ·5')
        self.check_name('ൺ·5 ̀')
        self.check_name('ൺ·5 ̀‿')

    def test_name_start_char(self):
        self.check_name('?A')
        self.check_name('?A_')
        self.check_name('?A_z')
        self.check_name('?A_zÊ')
        self.check_name('?A_zÊÝ')
        self.check_name('?A_zÊÝĄ')
        self.check_name('?A_zÊÝĄͼ')
        self.check_name('?A_zÊÝĄͼൺ')
        self.check_name('?A_zÊÝĄͼൺ')
        self.check_name('?A_zÊÝĄͼൺ⁶')
        self.check_name('?A_zÊÝĄͼൺ⁶Ⰲ')
        self.check_name('?A_zÊÝĄͼൺ⁶Ⰲ〠')
        self.check_name('?A_zÊÝĄͼൺ⁶Ⰲ〠邏２')
        self.check_name('?A_zÊÝĄͼൺ⁶Ⰲ〠邏２𐎅')

    def check_name(self, name):
        self.check_parser(name, AST.Name(name))

    def test_arithmetic_negation(self):
        self.check_parser(NEGATION_STR, NEGATION_AST)
        self.check_parser('--2', AST.Negation(AST.Negation(AST.Number(2))))
        self.check_parser('- -2', AST.Negation(AST.Negation(AST.Number(2))))
        self.check_parser('-  -2', AST.Negation(AST.Negation(AST.Number(2))))

    def test_arithmetic_expression(self):
        self.check_parser('%s**true' % DATE_STR,
                          AST.Exp(DATE_AST, AST.Boolean(True)))
        self.check_parser('%s  **true' % NEGATION_STR,
                          AST.Exp(NEGATION_AST, AST.Boolean(True)))
        self.check_parser('%s  /true  **%s' % (NEGATION_STR, NAME_STR),
                          AST.Div(NEGATION_AST, AST.Exp(AST.Boolean(True), NAME_AST)))
        self.check_parser('%s  *true  **%s' % (NEGATION_STR, NAME_STR),
                          AST.Mul(NEGATION_AST, AST.Exp(AST.Boolean(True), NAME_AST)))
        self.check_parser('%s  +1.2  /true  **%s' % (NEGATION_STR, NAME_STR),
                          AST.Sum(NEGATION_AST, AST.Div(AST.Number(1.2), AST.Exp(AST.Boolean(True), NAME_AST))))
        self.check_parser(ARITHMETIC_EXPRESSION_STR, ARITHMETIC_EXPRESSION_AST)

    def test_simple_value(self):
        # self.check_simple_parser('ala.ma.kota', AST.QualifiedName(['ala', 'ma', 'kota']))
        # self.check_simple_parser('ala.ma.kota', AST.QualifiedName(['ala', 'ma', 'kota']))
        self.check_simple_parser(DATE_STR, AST.SimpleExpressions([DATE_AST]))

    def test_unary_tests(self):
        self.check_table_parser('null', AST.PositiveUnaryTests([AST.Null()]))
        self.check_table_parser(NOT_STR, NOT_AST)
        self.check_table_parser('-', AST.NoTest())

    def test_positive_unary_tests(self):
        # self.check_parser('%s in null' % ARITHMETIC_EXPRESSION_STR,
        #                   AST.In(ARITHMETIC_EXPRESSION_AST, AST.PositiveUnaryTests([AST.Null()])))
        self.check_parser('%s  in  null' % ARITHMETIC_EXPRESSION_STR,
                          AST.In(ARITHMETIC_EXPRESSION_AST, AST.PositiveUnaryTests([AST.Null()])))
        self.check_parser(POSITIVE_UNARY_TESTS_STR,
                          POSITIVE_UNARY_TESTS_AST)

    def test_positive_unary_test(self):
        self.check_parser(POSITIVE_UNARY_TEST_STR, POSITIVE_UNARY_TEST_AST)

    def test_simple_unary_tests(self):
        self._check_simple_unary_tests_parser(SIMPLE_POSITIVE_UNARY_TESTS_STR, SIMPLE_POSITIVE_UNARY_TESTS_AST)
        self._check_simple_unary_tests_parser('not (%s)' % SIMPLE_POSITIVE_UNARY_TESTS_STR,
                                              AST.Not(SIMPLE_POSITIVE_UNARY_TESTS_AST))
        self._check_simple_unary_tests_parser('-', AST.NoTest())

    def test_closed_interval_end(self):
        self.check_parser('1in]2..3]',
                          AST.In(AST.Number(1),
                                 AST.PositiveUnaryTests([AST.Interval(AST.OpenIntervalStart(),
                                                                      AST.Endpoint(AST.Number(2)),
                                                                      AST.Endpoint(AST.Number(3)),
                                                                      AST.ClosedIntervalEnd())])))

    def test_open_interval_end(self):
        self.check_parser('1 in ]2..3)',
                          AST.In(AST.Number(1),
                                 AST.PositiveUnaryTests([AST.Interval(AST.OpenIntervalStart(),
                                                                      AST.Endpoint(AST.Number(2)),
                                                                      AST.Endpoint(AST.Number(3)),
                                                                      AST.OpenIntervalEnd())])))
        self.check_parser('1 in ]2..3[',
                          AST.In(AST.Number(1),
                                 AST.PositiveUnaryTests([AST.Interval(AST.OpenIntervalStart(),
                                                                      AST.Endpoint(AST.Number(2)),
                                                                      AST.Endpoint(AST.Number(3)),
                                                                      AST.OpenIntervalEnd())])))

    def test_closed_interval_start(self):
        self.check_parser('1 in [2..3]',
                          AST.In(AST.Number(1),
                                 AST.PositiveUnaryTests([AST.Interval(AST.ClosedIntervalStart(),
                                                                      AST.Endpoint(AST.Number(2)),
                                                                      AST.Endpoint(AST.Number(3)),
                                                                      AST.ClosedIntervalEnd())])))

    def test_open_interval_start(self):
        self.check_parser('1 in (2..3]',
                          AST.In(AST.Number(1),
                                 AST.PositiveUnaryTests([AST.Interval(AST.OpenIntervalStart(),
                                                                      AST.Endpoint(AST.Number(2)),
                                                                      AST.Endpoint(AST.Number(3)),
                                                                      AST.ClosedIntervalEnd())])))
        self.check_parser('1 in ]2..3]',
                          AST.In(AST.Number(1),
                                 AST.PositiveUnaryTests([AST.Interval(AST.OpenIntervalStart(),
                                                                      AST.Endpoint(AST.Number(2)),
                                                                      AST.Endpoint(AST.Number(3)),
                                                                      AST.ClosedIntervalEnd())])))

    def test_simple_positive_unary_test(self):
        self.check_parser('1 in <2',
                          AST.In(AST.Number(1), AST.PositiveUnaryTests([AST.LtEp(AST.Endpoint(AST.Number(2)))])))
        self.check_parser('1 in <=2',
                          AST.In(AST.Number(1), AST.PositiveUnaryTests([AST.LteEp(AST.Endpoint(AST.Number(2)))])))
        self.check_parser('1 in >2',
                          AST.In(AST.Number(1), AST.PositiveUnaryTests([AST.GtEp(AST.Endpoint(AST.Number(2)))])))
        self.check_parser('1 in >=2',
                          AST.In(AST.Number(1), AST.PositiveUnaryTests([AST.GteEp(AST.Endpoint(AST.Number(2)))])))
