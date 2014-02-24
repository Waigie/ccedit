__author__ = 'Christoph Weygand'

from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)
from lepl import *


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


class LEPLParser:
    def __init__(self, choice_marker):

        #tokens
        self.word = Token("[A-Za-z0-9_]+")
        self.value = Token(UnsignedReal())
        self.symbol = Token("[^0-9A-Za-z\{\} \t\r\n"+choice_marker+"]")
        self.number = Optional(self.symbol('-')) + self.value
        self.c_bracket = Token("[\{\}]")
        self.choice_marker = Token(choice_marker)

        self.code, self.choice = Delayed(), Delayed()

        self.identifier = self.word > DimensionName
        self.alternative = ~self.choice_marker & self.code > Alternative
        self.alternatives = self.alternative[2:, ~self.symbol(",")] > Alternatives
        self.choice += ~self.choice_marker & self.identifier & ~self.symbol("<") & self.alternatives & ~self.symbol(">") > Choice
        self.code_snippet = (self.word | self.number | self.symbol) > CodeSnippet
        self.code_block = ~self.c_bracket("{") & (self.choice | self.code_snippet)[:] & ~self.c_bracket("}") > CodeBlock
        self.code += (self.choice | self.code_snippet | self.code_block)[1:] > Code

    def parse(self, input):
        result = self.code.parse(input)
        if len(result) > 0:
            return result[0]
        else:
            return None