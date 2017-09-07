from FEELparser import FeelParser


def evaluate_ast(ast):
    pass


def evaluate(expression):
    parser = FeelParser()
    ast = parser.parse(expression, debug=True)
    return evaluate_ast(ast)
