__author__ = 'Christoph'

import unittest
import CCLang.Parser
import CCLang.Lens


class TestCCLangEquiv(unittest.TestCase):
    def setUp(self):
        self.parser = CCLang.Parser.LEPLParser("#")

        self.to_choice_ast = self.parser.parse('#B< 8 #, 9 #>')

        self.equiv = [
            ["#A< 1 #, 1 #>",                                     "1"],
            ["1",                                                 "#B<1 #, 1 #>"],
            ["#A< 1 #, 1 #>",                                     "#B<1 #, 1 #>"],
            ["#A< g( 1 ) #, g( 2 ) #>",                           "g ( #A< 1 #, 2 #> )"]
            #TODO: talk about what is expected here. Config A:3 is not definied for right expression
            #["#A< 1 #, 1 #, 1 #>",                                "#A<1 #, 1 #>"],
        ]

        self.nequiv = [
            #["#A< 1 #, 2 #>",                                     "#B<1 #, 2 #>"]
        ]

    def test_equiv(self):
        for left, right in self.equiv:
            right_ast = self.parser.parse(right)
            left_ast = self.parser.parse(left)
            self.assertTrue(left_ast.equiv(right_ast))

    def test_nequiv(self):
        for left, right in self.nequiv:
            right_ast = self.parser.parse(right)
            left_ast = self.parser.parse(left)
            self.assertFalse(left_ast.equiv(right_ast))
