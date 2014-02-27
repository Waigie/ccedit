__author__ = 'Christoph Weygand'

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
        self.t_word = Token("[A-Za-z0-9_]+")
        self.t_abracket = Token("[<>]")
        self.t_choice_marker = Token(choice_marker)
        self.t_value = Token(UnsignedReal())
        self.t_symbol = Token("[^"+choice_marker+"0-9A-Za-z<> \t\r\n]")
        self.t_number = Optional(self.t_symbol('-')) + self.t_value
        self.t_comma = Token(",")

        self.code, self.choice = Delayed(), Delayed()

        self.identifier = self.t_word > DimensionName
        self.alternative = ~self.t_choice_marker & self.code > Alternative
        self.alternatives = self.alternative[2:, ~self.t_comma] > Alternatives
        self.choice += ~self.t_choice_marker & self.identifier & ~self.t_abracket("<") & self.alternatives & ~self.t_abracket(">") > Choice
        self.code_snippet = (self.t_word | self.t_number | self.t_symbol)
        self.code += (self.choice | self.code_snippet)[1:] > Code

    def parse(self, input):
        result = self.code.parse(input)
        if len(result) > 0:
            return result[0]
        else:
            return None