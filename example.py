from feel.parser.OldParser import parser, tableParser, simpleParser, simpleUnaryTestsParser

input = 'x = function(x, y)\n' \
        '{\n' \
        '   "a": (x) instance  of  some.type,\n' \
        '   "b": if  some  z  in  [1..y[ satisfies  z  between 0 and 10\n' \
        '        then (1+2*3**4)\n' \
        '        else (date("12-12-12"))\n' \
        '}'

input = '1'

print(parser.parse(input))
