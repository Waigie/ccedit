__author__ = 'Waigie'

import unittest
import CCLang.Parser
from CCLang.ASTElements import *


class TestCCLangParser(unittest.TestCase):
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

    def test_no_meta_language(self):
        result = self.parser.parse('void testFunction() {}')
        self.assertTrue(self.only_code_ast.equiv(result))

    def test_simple_cc(self):
        result = self.parser.parse('#A<1#,2#,3#>')
        self.assertTrue(self.simple_ast.equiv(result))

    def test_nested_cc(self):
        result = self.parser.parse('#A< 1 #, #B< 2 #, 3 #> #>')
        self.assertEqual(result, self.complex_ast)

if __name__ == '__main__':
    unittest.main()