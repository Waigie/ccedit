__author__ = 'Waigie'

import unittest
import CCLang.Parser
import CCLang.ASTElements


class TestCCLangParser(unittest.TestCase):
    def setUp(self):
        self.parser = CCLang.Parser.LEPLParser("#")

    def test_no_meta_language(self):
        result = self.parser.parse('void testFunction() {}')
        self.assertEqual(result, CCLang.ASTElements.Code(['void', 'testFunction', '(', ')', '{', '}']))

    def test_simple_cc(self):
        expected_result = CCLang.ASTElements.Code([
            CCLang.ASTElements.Choice([
                CCLang.ASTElements.DimensionName(['A']),
                CCLang.ASTElements.Alternatives([
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['1'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['2'])]),
                    CCLang.ASTElements.Alternative([CCLang.ASTElements.Code(['3'])]),
                ])
            ])
        ])
        result = self.parser.parse('#A<1#,2#,3#>')
        self.assertEqual(result, expected_result)

    def test_nested_cc(self):
        expected_result = CCLang.ASTElements.Code([
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
        result = self.parser.parse('#A< 1 #, #B< 2 #, 3 #> #>')
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()