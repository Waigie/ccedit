__author__ = 'Waigie'

import unittest
import CCLang.Parser
import CCLang.Lens


class TestCCLangLens(unittest.TestCase):
    def setUp(self):
        self.parser = CCLang.Parser.LEPLParser("#")
        self.ast1 = self.parser.parse("#A< 1 #, 2 #>")
        self.ast2 = self.parser.parse("#A< 1 #, #B< 2 #, 3 #> #>")
        self.ast3 = self.parser.parse("#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>")

        self.to_choice_ast = self.parser.parse('#B< 8 #, 9 #>')

        self.leaves = [
            ["#A< 1 #, 2 #>",                          {"A": [0]},           "3",            "#A< 3 #, 2 #>"],
            ["#A< 1 #, 2 #>",                          {"A": [1]},           "3",            "#A< 1 #, 3 #>"],
            ["#A< 1 #, 2 #>",                          {"A": [0]},           "#B<3 #, 4 #>", "#A< #B<3 #, 4 #> #, 2 #>"],
            ["#A< 1 #, 2 #>",                          {"A": [1]},           "#B<3 #, 4 #>", "#A< 1 #, #B< 3 #, 4 #> #>"],
            ["#A< 1 #, #B< 2 #, 3 #> #>",              {"A": [0]},           "4",            "#A< 4 #, #B< 2 #, 3 #> #>"],
            ["#A< 1 #, #B< 2 #, 3 #> #>",              {"A": [0]},           "#B<4 #, 5 #>", "#A< #B<4 #, 5 #> #, #B< 2 #, 3 #> #>"],
            ["#A< 1 #, #B< 2 #, 3 #> #>",              {"A": [1], "B": [0]}, "4",            "#A< 1 #, #B< 4 #, 3 #> #>"],
            ["#A< 1 #, #B< 2 #, 3 #> #>",              {"A": [1], "B": [1]}, "4",            "#A< 1 #, #B< 2 #, 4 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"A": [0], "B": [0]}, "5",            "#A< #B< 5 #, 2 #> #, #B< 3 #, 4 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"A": [0], "B": [1]}, "5",            "#A< #B< 1 #, 5 #> #, #B< 3 #, 4 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"A": [1], "B": [0]}, "5",            "#A< #B< 1 #, 2 #> #, #B< 5 #, 4 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",  {"A": [1], "B": [1]}, "5",            "#A< #B< 1 #, 2 #> #, #B< 3 #, 5 #> #>"],
            ["#A< g( 1 ) #, 2 #>",                     {"A": [1]},           "g( 2 )",       "#A< g( 1 ) #, g( 2 ) #>"]
        ]

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

        self.implict = [
            ["1",                            {"A": [0]},           "2",              "#A< 2 #, 1 #>"],
            ["1",                            {"A": [1]},           "2",              "#A< 1 #, 2 #>"],
            ["1",                            {"A": [0], "B": [0]}, "2",              "#A< #B< 2 #, 1 #> #, 1 #>"],
            ["1",                            {"A": [0], "B": [1]}, "2",              "#A< #B< 1 #, 2 #> #, 1 #>"],
            ["1",                            {"A": [1], "B": [0]}, "2",              "#A< 1 #, #B< 2 #, 1 #> #>"],
            ["1",                            {"A": [1], "B": [1]}, "2",              "#A< 1 #, #B< 1 #, 2 #> #>"],
            ["#A< 1 #, #B< 2 #, 3 #> #>",    {"B": [0]},           "#A< 4 #, 5 #>",  "#A< #B< 4 #, 1 #> #, #B< 5 #, 3 #> #>"],
            ["#A< 1 #, #B< 2 #, 3 #> #>",    {"B": [1]},           "#A< 4 #, 5 #>",  "#A< #B< 1 #, 4 #> #, #B< 2 #, 5 #> #>"],
        ]

        self.tricky = [
            ["#A< 1 #, #B< 2 #, 3 #> #>",               {"B": [0]},   "4",    "#B< 4 #, #A< 1 #, 3 #> #>"],
            ["#A< 1 #, #B< 2 #, 3 #> #>",               {"B": [1]},   "4",    "#B< #A< 1 #, 2 #> #, 4 #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",   {"B": [0]},   "5",    "#A< #B< 5 #, 2 #> #, #B< 5 #, 4 #> #>"],
            ["#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>",   {"B": [1]},   "5",    "#A< #B< 1 #, 5 #> #, #B< 3 #, 5 #> #>"],
        ]

        self.arity = [
            ["#A< 1 #, 2 #>",               {},   "#A< 1 #, 2 #, 3 #>",    "#A< 1 #, 2 #, 3 #>"],
            ["#A< 1 #, 2 #, 3#>",           {},   "#A< 1 #, 2 #>",         "#A< 1 #, 2 #>"],
        ]

    def test_leaves(self):
        for old, config, new, expected_src in self.leaves:
            expected = self.parser.parse(expected_src)
            new_ast = CCLang.Lens.update(config, self.parser.parse(old), self.parser.parse(new))
            self.assertTrue(expected.equiv(new_ast), "Got %s expected %s" % (new_ast.apply_and_print({}, "#"), expected_src))

    def test_subs(self):
        for old, config, new, expected_src in self.subs:
            expected = self.parser.parse(expected_src)
            new_ast = CCLang.Lens.update(config, self.parser.parse(old), self.parser.parse(new))
            self.assertTrue(expected.equiv(new_ast), "Got %s expected %s" % (new_ast.apply_and_print({}, "#"), expected_src))

    def test_implict(self):
        for old, config, new, expected_src in self.implict:
            expected = self.parser.parse(expected_src)
            new_ast = CCLang.Lens.update(config, self.parser.parse(old), self.parser.parse(new))
            self.assertTrue(expected.equiv(new_ast), "Got %s expected %s" % (new_ast.apply_and_print({}, "#"), expected_src))

    def test_tricky(self):
        for old, config, new, expected_src in self.tricky:
            expected = self.parser.parse(expected_src)
            new_ast = CCLang.Lens.update(config, self.parser.parse(old), self.parser.parse(new))
            self.assertTrue(expected.equiv(new_ast), "Got %s expected %s" % (new_ast.apply_and_print({}, "#"), expected_src))

    def test_arity(self):
        for old, config, new, expected_src in self.arity:
            expected = self.parser.parse(expected_src)
            new_ast = CCLang.Lens.update(config, self.parser.parse(old), self.parser.parse(new))
            self.assertTrue(expected.equiv(new_ast), "Got %s expected %s" % (new_ast.apply_and_print({}, "#"), expected_src))
