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

    def test_ast1_change_left(self):
        expected = self.parser.parse("#A< 3 #, 2 #>")
        new_ast = CCLang.Lens.update({"A": [0]}, self.ast1, Code("3"))
        print(new_ast.pretty_print({}, ""))
        self.assertEqual(new_ast, expected)

    def test_ast1_change_right(self):
        expected = self.parser.parse("#A< 1 #, 3 #>")
        new_ast = CCLang.Lens.update({"A": [1]}, self.ast1, Code("3"))
        print(new_ast.pretty_print({}, ""))
        self.assertEqual(new_ast, expected)

    def test_ast1_change_left_to_choice(self):
        expected = self.parser.parse("#A< #B< 8 #, 9 #> #, 2 #>")
        new_ast = CCLang.Lens.update({"A": [0]}, self.ast1, self.to_choice_ast)
        print(new_ast.pretty_print({}, ""))
        self.assertEqual(new_ast, expected)

    def test_ast1_change_right_to_choice(self):
        expected = Code([
            Choice([DimensionName(["A"]), Alternatives([
                    Alternative([Code(["1"])]),
                    Alternative([self.to_choice_ast])
            ])])
        ])

        new_ast = CCLang.Lens.update({"A": [1]}, self.ast1, self.to_choice_ast)
        print(new_ast.pretty_print({}, ""))
        self.assertEqual(new_ast, expected)

    def test_ast2_change_left(self):
        expected = self.parser.parse("#A< 4 #, #B< 2 #, 3 #> #>")
        new_ast = CCLang.Lens.update({"A": [0]}, self.ast2, Code(["4"]))
        print(new_ast.pretty_print({}, ""))
        self.assertEqual(new_ast, expected)

    def test_ast2_change_left_to_choice(self):
        expected = self.parser.parse("#A< #B< 8 #, 9 #> #, #B< 2 #, 3 #> #>")
        new_ast = CCLang.Lens.update({"A": [0]}, self.ast2, self.to_choice_ast)
        print(new_ast.pretty_print({}, ""))
        self.assertEqual(new_ast, expected)

    def test_ast2_change_2_selects(self):
        expected = self.parser.parse("#A< 1 #, #B< 4 #, 3 #> #>")
        new_ast = CCLang.Lens.update({"A": [0], "B": [1]}, self.ast2, Code(["4"]))
        print(new_ast.pretty_print({}, ""))
        self.assertEqual(new_ast, expected)

"""
 Edits that only change leaves. Correct behavior is obvious.

 leaves = [
  testCase "A<1,2>"           "A.l"     "1"      "3"      "A<3,2>",
  testCase "A<1,2>"           "A.r"     "2"      "3"      "A<1,3>",
  testCase "A<1,2>"           "A.l"     "1"      "B<3,4>" "A<B<3,4>,2>",
  testCase "A<1,2>"           "A.r"     "2"      "B<3,4>" "A<1,B<3,4>>",
  testCase "A<1,B<2,3>>"      "A.l"     "1"      "4"      "A<4,B<2,3>>",
  testCase "A<1,B<2,3>>"      "A.l"     "1"      "B<4,5>" "A<B<4,5>,B<2,3>>",
  testCase "A<1,B<2,3>>"      "A.r,B.l" "2"      "4"      "A<1,B<4,3>>",
  testCase "A<1,B<2,3>>"      "A.r,B.r" "3"      "4"      "A<1,B<2,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.l,B.l" "1"      "5"      "A<B<5,2>,B<3,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.l,B.r" "2"      "5"      "A<B<1,5>,B<3,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.r,B.l" "3"      "5"      "A<B<1,2>,B<5,4>>",
  testCase "A<B<1,2>,B<3,4>>" "A.r,B.r" "4"      "5"      "A<B<1,2>,B<3,5>>"]
"""