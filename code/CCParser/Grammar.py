__author__ = 'Waigie'

from modgrammar import *


class Identifier(Grammar):
    grammar = (WORD("A-Z", "a-z"))


class Instance(Grammar):
    grammar = (Identifier, LITERAL("<"), REPEAT(ANY), LITERAL(">"))


class Choice(Grammar):
    grammar = (LITERAL("{"), REPEAT(ANY), LITERAL("}"))


class Choices(Grammar):
    grammar = (Choice, LITERAL(","), Choice)

parser = Instance.parser()
result = parser.parse_string("Choice<a,b>")

parser = Choice.parser()
result = parser.parse_string("{a}, {b}")
print(result.elements)
