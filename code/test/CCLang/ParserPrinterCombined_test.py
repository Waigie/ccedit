__author__ = 'Waigie'

import unittest
import CCLang.Parser
import CCLang.ASTElements


class TestParserPrinterCombined(unittest.TestCase):

    def setUp(self):
        self.parser = CCLang.Parser.LEPLParser("#")

    def test_combined_code(self):
        ast = CCLang.ASTElements.Code(['void', 'testFunction', '(', ')', '{', '}'])
        print_result = ast.pretty_print({}, '#')
        result = self.parser.parse(print_result)
        self.assertEqual(ast, result)

    def test_combined_simple_cc(self):
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
        print_result = ast.pretty_print({}, '#')
        result = self.parser.parse(print_result)
        self.assertEqual(ast, result)

    def test_combined_nested_cc(self):
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
        print_result = ast.pretty_print({}, '#')
        result = self.parser.parse(print_result)
        self.assertEqual(ast, result)
