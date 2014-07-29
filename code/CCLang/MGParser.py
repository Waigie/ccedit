__author__ = 'Waigie'

from modgrammar import *

#modgrammar implementation
grammar_whitespace_mode = 'optional'


class MetaMarker(Grammar):
    meta_marker = '#'
    grammar = (L(meta_marker))

    def set_meta_marker(self, meta_marker):
        self.meta_marker = meta_marker


class Identifier(Grammar):
    grammar = (WORD("A-Za-z0-9_"))


class Alternatives(Grammar):
    grammar = (LIST_OF(REF("Code"), sep=(MetaMarker, L(",")), min=2))


class Dimension(Grammar):
    grammar = (MetaMarker, Identifier, L("<"), Alternatives, MetaMarker, L(">"))


class CodeSnippet(Grammar):
    grammar = (ANY_EXCEPT("#"))


class Code(Grammar):
    grammar = (REPEAT(Dimension | CodeSnippet) | EMPTY)


def parse(code):
    parser = Code.parser()
    return parser.parse_text(code, reset=True, eof=True, matchtype='complete')
