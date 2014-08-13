__author__ = 'Christoph Weygand <christophweygand@gmail.com>'

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
                        Code(['1']),
                        Code(['2']),
                        Code(['3']),
                    ])
                ])
        ])
        self.complex_ast = Code([Choice([DimensionName(['A']),
                Alternatives([
                    Code(['1']),
                    Code([
                        Choice([
                            DimensionName(['B']),
                            Alternatives([
                                Code(['2']),
                                Code(['3']),
                            ])
                        ])
                    ])
                ])
        ])])


    def test_combined_code(self):
        ast = self.only_code_ast
        print_result = ast.apply_and_print({}, '#')
        result = self.parser.parse(print_result)
        self.assertTrue(ast.equiv(result))

    def test_combined_simple_cc(self):
        ast = self.simple_ast
        print_result = ast.apply_and_print({}, '#')
        result = self.parser.parse(print_result)
        self.assertTrue(ast.equiv(result))

    def test_combined_nested_cc(self):
        ast = self.complex_ast
        print_result = ast.apply_and_print({}, '#')
        result = self.parser.parse(print_result)
        self.assertTrue(ast.equiv(result))
