__author__ = 'Christoph Weygand <christophweygand@gmail.com>'

import unittest
import CCLang.Parser
import CCLang.Lens
from CCLang.ASTElements import *


class TestCCLangLens(unittest.TestCase):
    def setUp(self):
        self.parser = CCLang.Parser.LEPLParser("#")
        self.ast1 = self.parser.parse("#A< 1 #, 2 #>")
        self.ast2 = self.parser.parse("#A< 1 #, #B< 2 #, 3 #> #>")
        self.ast3 = self.parser.parse("#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>")

        self.to_choice_ast = self.parser.parse('#B< 8 #, 9 #>')

    def test_ast1_change_left(self):
        expected = self.parser.parse("#A< 3 #, #A< 1 #, 2 #> #>")
        new_ast = CCLang.Lens.choice({"A": [0]}, self.ast1, Code(["3"]))
        self.assertTrue(expected.equiv(new_ast))

    def test_ast1_change_right(self):
        expected = self.parser.parse("#A< #A< 1 #, 2 #> #, 3 #>")
        new_ast = CCLang.Lens.choice({"A": [1]}, self.ast1, Code(["3"]))
        self.assertTrue(expected.equiv(new_ast))

    def test_ast1_change_left_to_choice(self):
        expected = self.parser.parse("#A< #B< 8 #, 9 #> #, #A< 1 #, 2 #> #>")
        new_ast = CCLang.Lens.choice({"A": [0]}, self.ast1, self.to_choice_ast)
        self.assertTrue(expected.equiv(new_ast))

    def test_ast1_change_right_to_choice(self):
        expected = self.parser.parse("#A< #A< 1 #, 2 #> #, #B< 8 #, 9 #> #>")
        new_ast = CCLang.Lens.choice({"A": [1]}, self.ast1, self.to_choice_ast)
        self.assertTrue(expected.equiv(new_ast))
