__author__ = 'Waigie'

import unittest
import CCLang.Parser
from CCLang.ASTElements import *


class TestParserPrinterCombined(unittest.TestCase):

    def setUp(self):
        self.parser = CCLang.Parser.LEPLParser("#")
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


    def test_combined_code(self):
        ast = self.only_code_ast
        print_result = ast.pretty_print({}, '#')
        result = self.parser.parse(print_result)
        self.assertEqual(ast, result)

    def test_combined_simple_cc(self):
        ast = self.simple_ast
        print_result = ast.pretty_print({}, '#')
        result = self.parser.parse(print_result)
        self.assertEqual(ast, result)

    def test_combined_nested_cc(self):
        ast = self.complex_ast
        print_result = ast.pretty_print({}, '#')
        result = self.parser.parse(print_result)
        self.assertEqual(ast, result)
