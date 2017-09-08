from feel.parser.parser.Parser import parser
from feel.parser.simple.SimpleParser import parser as simple_parser
from feel.parser.table.TableParser import parser as table_parser


inp = 'x = function(x, y)\n' \
        '{\n' \
        '   "a": (x) instance  of  some.type,\n' \
        '   "b": if  z  in  [1..y[\n' \
        '        then (1+2*3**4)\n' \
        '        else (date("12-12-12")),\n' \
        '   "c": if  some  z  in  array  satisfies (2 ** y > z)\n' \
        '        then  z(1,2,3)\n' \
        '        else  z(a=1,c=3,b=2)\n' \
        '}'

print(parser.parse(inp, debug=False))

inp2 = '1 + 2 < x'

print(simple_parser.parse(inp2))

inp3 = 'not (<= 2, null, "asd")'

print(table_parser.parse(inp3, debug=False))
