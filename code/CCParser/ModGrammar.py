__author__ = 'Christoph Weygand'

from modgrammar import *


class Identifier(Grammar):
    grammar = (WORD("A-Z", "a-zA-Z0-9"))


class Choice(Grammar):
    grammar = (REPEAT(ANY, greedy=False))


class Choices(Grammar):
    grammar = (Choice, REPEAT((OPTIONAL(REPEAT(SPACE)), LITERAL(","), OPTIONAL(REPEAT(SPACE)), Choice), greedy=False))


class Instance(Grammar):
    grammar = (Identifier, LITERAL("<"), Choices, LITERAL(">"))


class Codeblock(Grammar):
    grammar = (REPEAT(ANY))


class CCCode(Grammar):
    grammar = (REPEAT((Instance | Codeblock), greedy=False))


parser = CCCode.parser()
result = parser.parse_string(""
                             "Choice<a,b>\n"
                             "foobar\n"
                             "Choice<c,d>")
print(result.terminals())