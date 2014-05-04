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

    def test_no_meta_language(self):
        result = self.parser.parse('void testFunction() {}')
        self.assertEqual(result, self.only_code_ast)

    def test_simple_cc(self):
        result = self.parser.parse('#A<1#,2#,3#>')
        self.assertEqual(result, self.simple_ast)

    def test_nested_cc(self):
        result = self.parser.parse('#A< 1 #, #B< 2 #, 3 #> #>')
        self.assertEqual(result, self.complex_ast)

if __name__ == '__main__':
    unittest.main()