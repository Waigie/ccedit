__author__ = 'Christoph Weygand <christophweygand@gmail.com>'

import unittest
import CCLang.Parser
import CCLang.Lens
from CCLang.ASTElements import *


class TestCCLangMinimize(unittest.TestCase):

    def setUp(self):
        self.parser = CCLang.Parser.LEPLParser("#")
        self.ast0 = self.parser.parse("#A< 2  #, 3 #>")
        self.ast1 = self.parser.parse("#A< #A< 1 #, 2 #>  #, 3 #>")
        self.ast2 = self.parser.parse("#A< #A< 1 #, 2 #> #, #B< 2 #, 3 #> #>")

    def test_ast0(self):
        minimized = CCLang.Lens.minimize(self.ast0)
        self.assertEqual(self.ast0, minimized)

    def test_ast1(self):
        expected = self.parser.parse("#A< 1 #, 3 #>")
        minimized = CCLang.Lens.minimize(self.ast1)
        self.assertEqual(expected, minimized)

