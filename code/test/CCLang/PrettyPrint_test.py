__author__ = 'Waigie'

import unittest
import CCLang.ASTElements


class TestPrettyPrint(unittest.TestCase):

    def test_pretty_print_code_no_selection(self):
        ast = CCLang.ASTElements.Code(['void', 'testFunction', '(', ')', '{', '}'])
        self.assertEqual(ast.pretty_print({}, '#'), "void testFunction ( ) { } ")

    def test_pretty_print_choice_no_selection(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({}, '#'), "#A< 1 #, 2 #, 3 #> ")

    def test_pretty_print_nested_choices_no_selection(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code([
                        CCLang.ASTElements.Choice([
                            CCLang.ASTElements.DimensionName(['B']),
                            CCLang.ASTElements.Alternatives([
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                            ])
                        ])
                    ])])
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({}, '#'), "#A< 1 #, #B< 2 #, 3 #> #> ")

    def test_pretty_print_code_with_single_selection(self):
        ast = CCLang.ASTElements.Code(['void', 'testFunction', '(', ')', '{', '}'])
        self.assertEqual(ast.pretty_print({'A': [1]}, '#'), "void testFunction ( ) { } ")

    def test_pretty_print_choice_with_single_selection_first(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({'A': [0]}, '#'), "1 ")

    def test_pretty_print_choice_with_single_selection_second(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({'A': [1]}, '#'), "2 ")

    def test_pretty_print_choice_with_single_selection_last(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({'A': [2]}, '#'), "3 ")

    def test_pretty_print_nested_choices_with_selection_first(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code([
                        CCLang.ASTElements.Choice([
                            CCLang.ASTElements.DimensionName(['B']),
                            CCLang.ASTElements.Alternatives([
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                            ])
                        ])
                    ])])
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({'A': [0]}, '#'), "1 ")

    def test_pretty_print_nested_choices_with_selection_second(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code([
                        CCLang.ASTElements.Choice([
                            CCLang.ASTElements.DimensionName(['B']),
                            CCLang.ASTElements.Alternatives([
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                            ])
                        ])
                    ])])
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({'A': [1]}, '#'), "#B< 2 #, 3 #> ")

    def test_pretty_print_nested_choices_with_selection_second_first(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code([
                        CCLang.ASTElements.Choice([
                            CCLang.ASTElements.DimensionName(['B']),
                            CCLang.ASTElements.Alternatives([
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                            ])
                        ])
                    ])])
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({'A': [1], 'B': [0]}, '#'), "2 ")

    def test_pretty_print_nested_choices_with_selection_second_last(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code([
                        CCLang.ASTElements.Choice([
                            CCLang.ASTElements.DimensionName(['B']),
                            CCLang.ASTElements.Alternatives([
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                                CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                            ])
                        ])
                    ])])
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({'A': [1], 'B': [1]}, '#'), "3 ")

    def test_pretty_print_choices_with_selection_out_of_bound(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                ])
            ])
        ])
        self.assertRaises(ValueError, ast.pretty_print, {'A': [5]}, '#')

    def test_pretty_print_choices_with_multi_selection(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({'A': [0, 2]}, '#'), "#A< 1 #, 3 #> ")

    def test_pretty_print_choices_with_multi_same_selection(self):
        ast = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                ])
            ])
        ])
        self.assertEqual(ast.pretty_print({'A': [1, 1]}, '#'), "2 ")
