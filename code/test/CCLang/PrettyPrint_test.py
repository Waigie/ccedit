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

    def test_pretty_print_nested_choice_no_selection(self):
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
        self.assertEqual(ast.pretty_print({},'#'), "#A< 1 #, #B< 2 #, 3 #> #> ")