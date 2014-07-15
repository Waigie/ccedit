__author__ = 'Christoph Weygand'

from lepl import *
from CCLang.ASTElements import *
from modgrammar import *
import sys


class LEPLParser:
    def __init__(self, meta_marker):
        #log = getLogger('lepl')
        #tokens
        self.t_word = Token("[A-Za-z0-9_]+")
        self.t_meta_marker = Token(meta_marker)
        self.t_value = Token(UnsignedReal())
        self.t_symbol = Token("[^"+meta_marker+"0-9A-Za-z \t\r\n]")
        self.t_number = Optional(self.t_symbol('-')) + self.t_value
        self.t_newline = Token("\r?\n")
        self.t_tab = Token("\t")
        self.code, self.choice = Delayed(), Delayed()

        self.identifier = self.t_word > DimensionName
        self.alternative = self.code #> Alternative
        self.alternatives = self.alternative[2:, ~(self.t_meta_marker & self.t_symbol(","))] > Alternatives
        self.choice += ~self.t_meta_marker & self.identifier & ~self.t_symbol("<") & self.alternatives \
            & ~self.t_meta_marker & ~self.t_symbol(">") > Choice
        self.code_snippet = (self.t_word | self.t_number | self.t_symbol | self.t_newline | self.t_tab)
        self.code += (self.choice | self.code_snippet)[1:] > Code

    def parse(self, code):
        result = self.code.parse(code)
        if len(result) > 0:
            return result[0]
        else:
            return None


# #modgrammar implementation
# grammar_whitespace_mode = 'optional'
#
#
# class MetaMarker(Grammar):
#     meta_marker = '#'
#     grammar = (L(meta_marker))
#
#     def set_meta_marker(self, meta_marker):
#         self.meta_marker = meta_marker
#
#
# class Identifier(Grammar):
#     grammar = (WORD("A-Za-z0-9_"))
#
#
# class Alternatives(Grammar):
#     grammar = (LIST_OF(REF("Code"), sep=(MetaMarker, L(",")), min=2))
#
#
# class Dimension(Grammar):
#     grammar = (MetaMarker, Identifier, L("<"), Alternatives, MetaMarker, L(">"))
#
#
# class CodeSnippet(Grammar):
#     grammar = (ANY_EXCEPT("#"))
#
#
# class Code(Grammar):
#     grammar = REPEAT(Dimension | CodeSnippet)
#
#
# def parse(code):
#     parser = Code.parser()
#     return parser.parse_text(code, reset=True, eof=True, matchtype='complete')