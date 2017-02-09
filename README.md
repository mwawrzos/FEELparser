# FEELparser
Python version of FEEL parser.

Feel is a part of DMN. It's doccumentation can be found here: http://www.omg.org/spec/DMN/

# Used technologies
This parser is based on PLY. There is a lexing module (`FEELlexer.py`) and a parsing one (`FEELparser.py`).
Parsing rules are tested using `unittest` package.
## Lexer
Lexing module has an variable named `lexer`. It is used to tokenize FEEL files. To tokenize some text, use 
```python
lexer.input(<FEELsource>)
```
Tokens extracted from text can by accessed using `for` loop:
```python
for tok in lexer:
  print tok
```

## Parser
Parser module already uses lexing module and is properly binded. Parser is defined as a class.
When creating instance of a parser, you can pass arguments related with `ply.yacc`. They will be passed to it.
Only argument `module` can't be used, as it is utilised by `FEELparser`.

Example usage of arguments is changing the starting rule. It could be usefull for debugging purposes:
```python
parser = FeelParser(start='arithmetic_expression')
```
Parser created that way will only parse arithmetic expressions, and whole AST will be rooted on such expressions.

The most common way to use FEELparser is presented in `test1.py` module.
  - create parser `parser = FeelParser()`
  - parse some expression `ast = parser.parse('1 + 2')`
  
When expression is correct, some AST will be returned. In other way, `None` object is returned and some log is printed.

## Tests
This library is fully tested. You can check it just running a command `python test1.py`.
You can find in that file, what AST sould be generated, for several expressions.

# Missing elements
Parser lacks in good error reporting. Current logs are understable only by author. Further works will be focused on that topic.
