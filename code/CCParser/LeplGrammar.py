__author__ = 'Christoph Weygand'

from logging import basicConfig, DEBUG, ERROR
basicConfig(level=ERROR)
from lepl import *

# codeSnippet, instance = Delayed(), Delayed()

# optSpaces = ~Space()[0:]
# identifier = Word(Upper(), (Upper() | Lower() | Digit())) > Identifier
# choice = optSpaces & (instance | codeSnippet) & optSpaces > Choice
# choices = choice & (~Literal(",") & optSpaces & choice)[1:] > Choices
# instance += identifier & ~Literal("<") & optSpaces & choices & optSpaces & ~Literal(">") > Instance
# codeSnippet += Word() > Code
# file = (instance | codeSnippet) & (optSpaces & (instance | codeSnippet))[:] > File
#
#
# def parse(input_code):
#     result = file.parse(input_code)
#     if len(result) > 0:
#         return result[0]
#     else:
#         return None

#tokens
word = Token("[A-Za-z0-9_]+")
value = Token(UnsignedReal())
symbol = Token("[^0-9A-Za-z\{\} \t\r\n]")
number = Optional(symbol('-')) + value
c_bracket = Token("[\{\}]")


class DimensionName(List):
    pass


class Choice(List):
    pass


class Alternatives(List):
    pass


class Alternative(List):
    pass


class CodeBlock(List):
    pass


class CodeSnippet(List):
    pass


class Code(List):
    pass


code, choice = Delayed(), Delayed()

identifier = word > DimensionName
alternative = ~c_bracket("{") & code & ~c_bracket("}") > Alternative
alternatives = alternative[2:, ~symbol(",")] > Alternatives
choice += identifier & ~symbol("<") & alternatives & ~symbol(">") > Choice
codeSnippet = (word | number | symbol) > CodeSnippet
codeBlock = ~c_bracket("{") & (choice | codeSnippet)[:] & ~c_bracket("}") > CodeBlock
code += (choice | codeSnippet | codeBlock)[1:] > Code


def parse(input_code):
    result = code.parse(input_code)
    if len(result) > 0:
        return result[0]
    else:
        return None

if __name__ == '__main__':
    result = code.parse('def twice(Parameter< {x}, {y}, {z} >):\n return Implementation< {Parameter<{x}, {y}, {z}>+Parameter< {x}, {y}, {z} >}, {2*Parameter< {x}, {y}, {z} >} >')
    print(result[0])
