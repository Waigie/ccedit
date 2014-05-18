__author__ = 'Waigie'

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

        self.subs = [
            ["#A< 1 #, #B< 2 #, 3 #> #>",              {"A": [1]}, "4",            "#A< 1 #, 4 #>"],
            ["#A< 1 #, #B< 2 #, 3 #> #>",              {"A": [1]}, "#B<4 #, 5 #>", "#A< 1 #, #B< 4 #, 5 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"A": [0]}, "5",            "#A< 5 #, #B< 3 #, 4 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"A": [1]}, "5",            "#A< #B< 1 #, 2 #> #, 5 #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"A": [0]}, "#B<5 #, 6 #>", "#A< #B< 5 #, 6 #> #, #B<3 #, 4 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"A": [1]}, "#B<5 #, 6 #>", "#A< #B< 1 #, 2 #> #, #B<5 #, 6 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"B": [0]}, "#A<5 #, 6 #>", "#A< #B< 5 #, 2 #> #, #B<6 #, 4 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"B": [1]}, "#A<5 #, 6 #>", "#A< #B< 1 #, 5 #> #, #B<3 #, 6 #> #>"],
        ]
        """
        Haskell result from last test mirrors python result, what is wrong?
        update (Config [("B", True)]) (readCC "A<B<1,2>,B<3,4>>") (readCC "A<5,6>")
        B<A<5,6>,A<2,4>>
        """


        """
        testCase "1"                "A.l"     "1"      "2"      "A<2,1>",
        testCase "1"                "A.r"     "1"      "2"      "A<1,2>",
        testCase "1"                "A.l,B.l" "1"      "2"      "A<B<2,1>,1>",
        testCase "1"                "A.l,B.r" "1"      "2"      "A<B<1,2>,1>",
        testCase "1"                "A.r,B.l" "1"      "2"      "A<1,B<2,1>>",
        testCase "1"                "A.r,B.r" "1"      "2"      "A<1,B<1,2>>",
        testCase "A<1,B<2,3>>"      "B.l"     "A<1,2>" "A<4,5>" "A<B<4,1>,B<5,3>>", -- was: A<4,B<5,3>>
        testCase "A<1,B<2,3>>"      "B.r"     "A<1,3>" "A<4,5>" "A<B<1,4>,B<2,5>>"]
        """
        self.implict = [
            #["1",       {"A": [0]},         "2",       "#A< 2 #, 1 #>"]
            ["#A< 1 #, 2 #> + #B< 3 #, 4 #>", {"A":[0], "B":[0]}, "a+b", "1"]
        ]


    def test_ast1_change_left(self):
        expected = self.parser.parse("#A< 3 #, 2 #>")
        new_ast = CCLang.Lens.update({"A": [0]}, self.ast1, Code("3"))
        self.assertEqual(new_ast, expected)


    def test_subs(self):
        for old, config, new, expected_src in self.subs:
            expected = self.parser.parse(expected_src)
            new_ast = CCLang.Lens.update(config, self.parser.parse(old), self.parser.parse(new))
            self.assertEqual(new_ast, expected, "Got %s expected %s" % (new_ast.pretty_print({}, "#"), expected_src))

    # def test_implict(self):
    #     for old, config, new, expected_src in self.implict:
    #         expected = self.parser.parse(expected_src)
    #         new_ast = CCLang.Lens.update(config, self.parser.parse(old), self.parser.parse(new))
    #         self.assertEqual(new_ast, expected, "Got %s expected %s" % (new_ast.pretty_print({}, "#"), expected_src))

