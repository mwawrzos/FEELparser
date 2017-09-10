class AST:
    def __init__(self, token):
        self.value = token

    def __eq__(self, o) -> bool:
        return self.__class__ == o.__class__ and self.value == o.value

    def __str__(self):
        return '%s{%s}' % (self.__class__.__name__, self.value)

    __repr__ = __str__


class Date(AST):
    pass


class Time(AST):
    pass


class DateAndTime(AST):
    pass


class Duration(AST):
    pass


class Name(AST):
    pass


class Context(AST):
    pass


class Param(AST):
    pass


class FunctionDefinition(AST):
    def __init__(self, params: [Param], external, body):
        super(FunctionDefinition, self).__init__(body)
        self.params = params
        self.external = external

    def __str__(self):
        return "function(%s)%s %s" % (self.params,
                                      'external' if self.external else '',
                                      super(FunctionDefinition, self).__str__())

    __repr__ = __str__

    def __eq__(self, o) -> bool:
        return super(AST, self).__eq__(o) and self.external == o.external and self.params == o.params


class List(AST):
    pass


class Type(AST):
    pass


class InstanceOf(AST):
    def __init__(self, expression, instance_type):
        super(InstanceOf, self).__init__(expression)
        self.type = instance_type

    def __str__(self):
        return "%s instance of %s" % (self.value, self.type)

    __repr__ = __str__

    def __eq__(self, o) -> bool:
        return super(InstanceOf, self).__eq__(o) and self.type == o.type


class QualifiedName(AST):
    pass


class FilterExpression(AST):
    def __init__(self, token, filter_value):
        super(FilterExpression, self).__init__(token)
        self.filter = filter_value

    def __eq__(self, o) -> bool:
        return super(FilterExpression, self).__eq__(o) and self.filter == o.filter

    def __str__(self):
        return '%s[%s]' % (self.value, self.filter)

    __repr__ = __str__


class BinOp(AST):
    def __init__(self, lhs, op, rhs):
        super(BinOp, self).__init__(lhs)
        self.op = op
        self.rhs = rhs

    def __eq__(self, o) -> bool:
        return super(BinOp, self).__eq__(o) and self.op == o.op and self.rhs == o.rhs

    def __str__(self):
        return '(%s %s %s)' % (self.value, self.op, self.rhs)

    __repr__ = __str__


class Eq(BinOp):
    def __init__(self, lhs, rhs):
        super(Eq, self).__init__(lhs, '=', rhs)


class Neq(BinOp):
    def __init__(self, lhs, rhs):
        super(Neq, self).__init__(lhs, '!=', rhs)


class Lt(BinOp):
    def __init__(self, lhs, rhs):
        super(Lt, self).__init__(lhs, '<', rhs)


class Lte(BinOp):
    def __init__(self, lhs, rhs):
        super(Lte, self).__init__(lhs, '<=', rhs)


class Gt(BinOp):
    def __init__(self, lhs, rhs):
        super(Gt, self).__init__(lhs, '<=', rhs)


class Gte(BinOp):
    def __init__(self, lhs, rhs):
        super(Gte, self).__init__(lhs, '<=', rhs)


class Between(AST):
    def __init__(self, token, b_start, b_end):
        super(Between, self).__init__(token)
        self.b_start = b_start
        self.b_end = b_end

    def __eq__(self, o) -> bool:
        return super(Between, self).__eq__(o) and self.b_start == o.b_start and self.b_end == o.b_end

    def __str__(self):
        return '{%s, %s, %s}' % (super(Between, self).__str__(), self.b_start, self.b_end)


class Null(AST):
    def __init__(self):
        super(Null, self).__init__(None)


class PositiveUnaryTests(AST):
    pass


class In(AST):
    def __init__(self, token, tests):
        super(In, self).__init__(token)
        self.tests = tests

    def __eq__(self, o) -> bool:
        return super(In, self).__eq__(o) and self.tests == o.tests

    def __str__(self):
        return '%s in %s' % (self.value, self.tests)

    __repr__ = __str__


class Conjunction(BinOp):
    def __init__(self, lhs, rhs):
        super(Conjunction, self).__init__(lhs, 'and', rhs)


class Disjunction(BinOp):
    def __init__(self, lhs, rhs):
        super(Disjunction, self).__init__(lhs, 'or', rhs)


class QuantifiedExpr(AST):
    def __init__(self, some, generators, test):
        super(QuantifiedExpr, self).__init__(some)
        self.generators = generators
        self.test = test

    def __eq__(self, o) -> bool:
        return super(QuantifiedExpr, self).__eq__(o) and self.generators == o.generators and self.test == o.test

    def __str__(self):
        return '%s %s satisfies %s' % ('some' if self.value else 'every',
                                       ' '.join('%s in %s' % p for p in self.generators),
                                       self.test)

    __repr__ = __str__


class If(AST):
    def __init__(self, condition, then, else_):
        super(If, self).__init__(condition)
        self.then = then
        self.else_ = else_

    def __eq__(self, o) -> bool:
        return super(If, self).__eq__(o) and self.then == o.then and self.else_ == o.else_

    def __str__(self):
        return 'if %s\n then %s\n else %s' % (self.value, self.then, self.else_)

    __repr__ = __str__


class For(AST):
    def __init__(self, generators, result):
        super(For, self).__init__(generators)
        self.result = result

    def __eq__(self, o) -> bool:
        return super(For, self).__eq__(o) and self.result == o.result

    def __str__(self):
        return 'for %s\n return %s' % (' '.join('%s in %s' % p for p in self.value),
                                       self.result)

    __repr__ = __str__


class Path(AST):
    def __init__(self, expr, name):
        super(Path, self).__init__(expr)
        self.name = name

    def __eq__(self, o) -> bool:
        return super(Path, self).__eq__(o) and self.name == o.name

    def __str__(self):
        return '%s.%s' % (self.value, self.name)

    __repr__ = __str__


class Invocation(AST):
    def __init__(self, foo, parameters):
        super(Invocation, self).__init__(foo)
        self.parameters = parameters

    def __eq__(self, o) -> bool:
        return super(Invocation, self).__eq__(o) and self.parameters == o.parameters

    def __str__(self):
        return '%s(%s)' % (self.value, ', '.join(str(p) for p in self.parameters))

    __repr__ = __str__


class Number(AST):
    pass


class Boolean(AST):
    pass


class StringLiteral(AST):
    pass


class Negation(AST):
    pass


class Exp(BinOp):
    def __init__(self, lhs, rhs):
        super(Exp, self).__init__(lhs, '**', rhs)


class Div(BinOp):
    def __init__(self, lhs, rhs):
        super(Div, self).__init__(lhs, '/', rhs)


class Mul(BinOp):
    def __init__(self, lhs, rhs):
        super(Mul, self).__init__(lhs, '*', rhs)


class Dif(BinOp):
    def __init__(self, lhs, rhs):
        super(Dif, self).__init__(lhs, '-', rhs)


class Sum(BinOp):
    def __init__(self, lhs, rhs):
        super(Sum, self).__init__(lhs, '+', rhs)


class Not(AST):
    pass


class NoTest(AST):
    def __init__(self):
        super(NoTest, self).__init__(None)


class IntervalBorders(AST):
    def __init__(self, representation):
        super(IntervalBorders, self).__init__(None)
        self.representation = representation

    def __str__(self):
        return self.representation

    __repr__ = __str__


class OpenIntervalStart(IntervalBorders):
    def __init__(self):
        super(OpenIntervalStart, self).__init__('(')


class ClosedIntervalStart(IntervalBorders):
    def __init__(self):
        super(ClosedIntervalStart, self).__init__('[')


class ClosedIntervalEnd(IntervalBorders):
    def __init__(self):
        super(ClosedIntervalEnd, self).__init__(']')


class OpenIntervalEnd(IntervalBorders):
    def __init__(self):
        super(OpenIntervalEnd, self).__init__(')')


class Endpoint(AST):
    pass


class Interval(AST):
    def __init__(self, start, start_value, end_value, end):
        super(Interval, self).__init__(start_value)
        self.start = start
        self.endValue = end_value
        self.end = end

    def __eq__(self, o) -> bool:
        rest = self.start == o.start and self.endValue == o.endValue and self.end == o.end
        return super(Interval, self).__eq__(o) and rest

    def __str__(self):
        return '%s%s..%s%s' % (self.start, self.value, self.endValue, self.end)

    __repr__ = __str__


class LtEp(AST):
    pass


class LteEp(AST):
    pass


class GtEp(AST):
    pass


class GteEp(AST):
    pass


class SimpleExpressions(AST):
    pass
