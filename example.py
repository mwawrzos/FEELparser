from feel.parser.parser.Parser import parser
from feel.parser.simple.SimpleParser import parser as simple_parser
from feel.parser.table.TableParser import parser as table_parser


inp = """
function (x, y)
{
    "a": (x) instance  of  some.type,
    "b": if  z  in [1..y[
         then (1+2*3**4)
         else (date("10-09-17")),
    "c": if  some  z  in  array  satisfies (2 ** y > z)
         then  z(1,2,3)
         else  z(a=1, c=3, b=2)
}
"""

print('some function definition tree:')
print(parser.parse(inp, debug=False))

inp2 = '1 + 2 < x'

print()
print('S-FEEL expression tree:')
print(simple_parser.parse(inp2))

print()
print('tree of input valid for tables only:')
inp3 = 'not (<= 2, null, "asd")'

print(table_parser.parse(inp3, debug=False))

inp4 = 'x = function(x, y)\n' \
        '{\n' \
        '   "a": (x) instance  of  some.type,\n' \
        '   "b": if  z  in  [1..y[\n' \
        '        the (1+2*3**4)\n' \
        '        else (date("12-12-12"))\n' \
        '   "c": if  some  z  in  array  satisfies (2 ** y > z)\n' \
        '        then  z(1,2,3)\n' \
        '        else  z(a=1,c=3,b=2)\n' \
        '}'

print()
print('diagnostics example:')
print(parser.parse(inp4))
