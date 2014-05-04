__author__ = 'Waigie'

import unittest
from CCLang.ASTElements import *


class TestPrettyPrint(unittest.TestCase):

    def setUp(self):
        self.only_code_ast = Code(['void', 'testFunction', '(', ')', '{', '}'])
        self.simple_ast = Code([
            Choice([DimensionName(['A']),
                    Alternatives([
                        Alternative([Code(['1'])]),
                        Alternative([Code(['2'])]),
                        Alternative([Code(['3'])]),
                    ])
                ])
        ])
        self.complex_ast = Code([Choice([DimensionName(['A']),
                Alternatives([
                    Alternative([Code(['1'])]),
                    Alternative([Code([
                        Choice([
                            DimensionName(['B']),
                            Alternatives([
                                Alternative([Code(['2'])]),
                                Alternative([Code(['3'])]),
                            ])
                        ])
                    ])])
                ])
        ])])


    def test_pretty_print_code_no_selection(self):
        self.assertEqual(self.only_code_ast.pretty_print({}, '#'), "void testFunction ( ) { } ")

    def test_pretty_print_choice_no_selection(self):
        self.assertEqual(self.simple_ast.pretty_print({}, '#'), "#A< 1 #, 2 #, 3 #> ")

    def test_pretty_print_nested_choices_no_selection(self):
        self.assertEqual(self.complex_ast.pretty_print({}, '#'), "#A< 1 #, #B< 2 #, 3 #> #> ")

    def test_pretty_print_code_with_single_selection(self):
        self.assertEqual(self.only_code_ast.pretty_print({'A': [1]}, '#'), "void testFunction ( ) { } ")

    def test_pretty_print_choice_with_single_selection_first(self):
        self.assertEqual(self.simple_ast.pretty_print({'A': [0]}, '#'), "1 ")

    def test_pretty_print_choice_with_single_selection_second(self):
        self.assertEqual(self.simple_ast.pretty_print({'A': [1]}, '#'), "2 ")

    def test_pretty_print_choice_with_single_selection_last(self):
        self.assertEqual(self.simple_ast.pretty_print({'A': [2]}, '#'), "3 ")

    def test_pretty_print_nested_choices_with_selection_first(self):
        self.assertEqual(self.complex_ast.pretty_print({'A': [0]}, '#'), "1 ")

    def test_pretty_print_nested_choices_with_selection_second(self):
        self.assertEqual(self.complex_ast.pretty_print({'A': [1]}, '#'), "#B< 2 #, 3 #> ")

    def test_pretty_print_nested_choices_with_selection_second_first(self):
        self.assertEqual(self.complex_ast.pretty_print({'A': [1], 'B': [0]}, '#'), "2 ")

    def test_pretty_print_nested_choices_with_selection_second_last(self):
        self.assertEqual(self.complex_ast.pretty_print({'A': [1], 'B': [1]}, '#'), "3 ")

    def test_pretty_print_choices_with_selection_out_of_bound(self):
        self.assertRaises(ValueError, self.simple_ast.pretty_print, {'A': [5]}, '#')

    def test_pretty_print_choices_with_multi_selection(self):
        self.assertEqual(self.simple_ast.pretty_print({'A': [0, 2]}, '#'), "#A< 1 #, 3 #> ")

    def test_pretty_print_choices_with_multi_same_selection(self):
        self.assertEqual(self.simple_ast.pretty_print({'A': [1, 1]}, '#'), "2 ")
