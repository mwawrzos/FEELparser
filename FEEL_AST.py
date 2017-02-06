def default_printer(obj, indent):
    return '\t' * indent + obj.__repr__()  # + ' :: ' + obj.__class__()


class NullAstNode(object):
    def __repr__(self):
        return self.pp(0)

    def pp(self, indent):
        return '%s%s' % ('\t' * indent, self.__class__)

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __ne__(self, other):
        return not self == other


class AstNode(NullAstNode):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return self.pp(0)

    def pp(self, indent):
        pp = pretty_printer(self.value)
        return '%s%s\n%s' % ('\t' * indent, self.__class__, pp(indent + 1))

    def __eq__(self, other):
        return super(AstNode, self).__eq__(other) and self.value == other.value


def pretty_printer(obj):
    kpp = getattr(obj, "pp", lambda i: default_printer(obj, i))
    return kpp


class AstBinaryNode(AstNode):
    def __init__(self, key=None, value=None):
        super(AstBinaryNode, self).__init__(value)
        self.key = key

    def __repr__(self):
        return self.pp(0)

    def pp(self, indent):
        kpp = pretty_printer(self.key)
        vpp = pretty_printer(self.value)
        return "%s%s\n%s\n%s" % (indent * '\t',
                                 self.__class__,
                                 kpp(indent + 1),
                                 vpp(indent + 1))

    def __eq__(self, other):
        return super(AstBinaryNode, self).__eq__(other) and self.key == other.key


class AstTernaryNode(AstBinaryNode):
    def __init__(self, expr=None, key=None, value=None):
        super(AstTernaryNode, self).__init__(key, value)
        self.expr = expr

    def __repr__(self):
        return self.pp(0)

    def pp(self, indent):
        epp = pretty_printer(self.expr)
        kpp = pretty_printer(self.key)
        vpp = pretty_printer(self.value)
        return '%s%s\n%s\n%s\n%s' % (indent * '\t',
                                     self.__class__,
                                     epp(indent + 1),
                                     kpp(indent + 1),
                                     vpp(indent + 1))

    def __eq__(self, other):
        return super(AstTernaryNode, self).__eq__(other) and self.expr == other.expr


# 1
class Expression(AstNode):
    pass


# 2
class TextualExpression(AstNode):
    pass


# 4
class ArithmeticExpression(AstNode):
    pass


# 15
class Null(NullAstNode):
    pass


# 21
class Addition(AstBinaryNode):
    pass


# 22
class Subtraction(AstBinaryNode):
    pass


# 23
class Multiplication(AstBinaryNode):
    pass


# 24
class Division(AstBinaryNode):
    pass


# 25
class Exponentiation(AstBinaryNode):
    pass


# 26
class ArithmeticNegation(AstNode):
    pass


# 27
class Name(AstNode):
    pass


# 33
class Literal(AstNode):
    pass


# 34
class SimpleLiteral(AstNode):
    pass


# 40
class FunctionInvocation(AstBinaryNode):
    pass


# 41
class PositionalParameters(AstNode):
    pass


# 42
class NamedParameters(AstNode):
    pass


# 45
class PathExpression(AstBinaryNode):
    pass


# 46
class ForExpression(AstBinaryNode):
    pass


# 47
class IfExpression(AstTernaryNode):
    pass


# 48
class QuantifiedExpression(AstBinaryNode):
    pass


class SomeQuantifiedExpression(QuantifiedExpression):
    pass


class EveryQuantifiedExpression(QuantifiedExpression):
    pass


# 49
class Disjunction(AstBinaryNode):
    pass


# 50
class Conjunction(AstBinaryNode):
    pass


# 51
class Comparison(AstNode):
    pass


# a
class Eq(AstBinaryNode):
    pass


class Neq(AstBinaryNode):
    pass


class Lt(AstBinaryNode):
    pass


class Lte(AstBinaryNode):
    pass


class Gt(AstBinaryNode):
    pass


class Gte(AstBinaryNode):
    pass


# b

class Between(AstTernaryNode):
    pass


# c
class In(AstBinaryNode):
    pass


# 52
class FilterExpression(AstBinaryNode):
    pass


# 53
class InstanceOf(AstBinaryNode):
    pass


# 55
class BoxedExpression(AstNode):
    pass


# 57
class FunctionDefinition(AstBinaryNode):
    pass


class ExternalFunctionDefinition(AstBinaryNode):
    pass


# 59
class Context(AstNode):
    def __eq__(self, other):
        return cmp(self.value, other.value) == 0


# 60
class ContextEntry(AstBinaryNode):
    pass


# 61
class Key(AstNode):
    pass


# 62
class DateLiteral(AstNode):
    pass


class TimeLiteral(AstNode):
    pass


class Date_And_TimeLiteral(AstNode):
    pass


class DurationLiteral(AstNode):
    pass
