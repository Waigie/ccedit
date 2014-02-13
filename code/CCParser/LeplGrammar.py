__author__ = 'Christoph Weygand'

from lepl import *


class Instance(List):
    pass


class Choices(List):
    pass


class Choice(List):
    pass


class Identifier(List):
    pass


class File(List):
    pass


class Code(List):
    pass

#tokens
codeSnippet, instance = Delayed(), Delayed()

optSpaces = ~Space()[0:]
identifier = Word(Upper(), (Upper() | Lower() | Digit())) > Identifier
choice = optSpaces & (instance | codeSnippet) & optSpaces > Choice
choices = choice & (~Literal(",") & optSpaces & choice)[1:] > Choices
instance += identifier & ~Literal("<") & optSpaces & choices & optSpaces & ~Literal(">") > Instance
codeSnippet += Word() > Code
file = (instance | codeSnippet) & (optSpaces & (instance | codeSnippet))[:] > File


def parse(input_code):
    result = file.parse(input_code)
    if len(result) > 0:
        return result[0]
    else:
        return None
