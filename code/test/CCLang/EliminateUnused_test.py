__author__ = 'Waigie'

import unittest
import CCLang.Parser
import CCLang.Lens


class TestCCLangEquiv(unittest.TestCase):
    def setUp(self):
        self.parser = CCLang.Parser.LEPLParser("#")

        self.to_choice_ast = self.parser.parse('#B< 8 #, 9 #>')

        self.equiv = [
            ["#A< 1 #, 1 #>",                                     "1"],
            ["#A< #B< 1 #, 1 #> #, 2 #>",                         "#A< 1 #, 2 #>"],
            ["#A< 1 #, #B< 2 #, 2 #> #>",                         "#A< 1 #, 2 #>"],
            ["#A< 1 #, #B< 1 #, 1 #> #>",                         "1"],
            ["#A< #B< 1 #, 1 #> #, 1 #>",                         "1"],
            ["#A< #B< 1 #, 2 #> #, #B< 1 #, 2 #> #>",             "#B< 1 #, 2 #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 2 #> #>",             "#A< #B< 1 #, 2 #> #, #B< 3 #, 2 #> #>"]
        ]

        self.nequiv = [

        ]

    def test_equiv(self):
        for left, right in self.equiv:
            right_ast = self.parser.parse(CCLang.Lens.eliminate_unused(right))
            left_ast = self.parser.parse(CCLang.Lens.eliminate_unused(left))
            self.assertTrue(left_ast.equiv(right_ast))

    def test_equiv(self):
        for left, right in self.equiv:
            right_ast = self.parser.parse(CCLang.Lens.eliminate_unused(right))
            left_ast = self.parser.parse(CCLang.Lens.eliminate_unused(left))
            self.assertFalse(left_ast.equiv(right_ast))