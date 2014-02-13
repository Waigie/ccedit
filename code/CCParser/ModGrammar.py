__author__ = 'Christoph Weygand'

from modgrammar import *


class Identifier(Grammar):
    grammar = (WORD("A-Z", "a-zA-Z0-9"))


class Choice(Grammar):
    grammar = (REF("CCCode"))


class RChoices(Grammar):
    grammar = (Choice, OPTIONAL((OPTIONAL(REPEAT(SPACE)), LITERAL(","), OPTIONAL(REPEAT(SPACE)), REF("RChoices"))))

class Choices(Grammar):
    grammar = (Choice, RChoices)


class Instance(Grammar):
    grammar = (Identifier, LITERAL("<"), Choices, LITERAL(">"))


class Codeblock(Grammar):
    grammar = (REPEAT(ANY, greedy=False))


class CCCode(Grammar):
    grammar = ((Instance | Codeblock), OPTIONAL(REF("CCCode")))


parser = CCCode.parser()
result = parser.parse_string("Choice<c,d>\nfoobar\nChoice<a,b>")
print(result.elements)