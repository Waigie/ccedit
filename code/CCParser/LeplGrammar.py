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
choice = ~Literal("{") & optSpaces & (instance | codeSnippet) & optSpaces & ~Literal("}") > Choice
choices = choice & (~Literal(",") & optSpaces & choice)[1:] > Choices
instance += identifier & ~Literal("<") & optSpaces & choices & optSpaces & ~Literal(">") > Instance
codeSnippet += Word() > Code
file = (instance | codeSnippet) & (optSpaces & (instance | codeSnippet))[:] > File

result = file.parse('code Choice<{ Choice2< { a }, { b } >},{foo}> more code Choice3<{c},{d}>')[0]
print(result)

