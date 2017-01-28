def default_printer(obj, indent):
    return '\t' * indent + obj.__repr__()  # + ' :: ' + obj.__class__()


class AstNode(object):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return self.pp(0)

    def pp(self, indent):
        pp = pretty_printer(self.value)
        return '\t' * indent + "%s\n%s" % (self.__class__, pp(indent + 1))

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
               and self.value == other.value


def pretty_printer(obj):
    kpp = getattr(obj, "pp", lambda i: default_printer(obj, i))
    return kpp


class AstBinaryNode(AstNode):
    def __init__(self, key=None, value=None):
        AstNode.__init__(self, value)
        self.key = key

    def __repr__(self):
        return self.pp(0)

    def pp(self, indent):
        kpp = pretty_printer(self.key)
        vpp = pretty_printer(self.value)
        return indent * '\t' + "%s\n%s\n%s" % (self.__class__,
                                               (kpp(indent + 1)),
                                               (vpp(indent + 1)))

    def __eq__(self, other):
        comparison = self.key == other.key and super(AstBinaryNode, self).__eq__(other)
        # print "%s\n==\n%s\n= %s" % (self, other, comparison)
        return comparison


# 1
class Expression(AstNode):
    pass


# 2
class TextualExpression(AstNode):
    pass


# 33
class Literal(AstNode):
    pass


# 34
class SimpleLiteral(AstNode):
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
