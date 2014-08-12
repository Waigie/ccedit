import CCLang.Parser
import CCLang.Lens

parser = CCLang.Parser.LEPLParser("#")
source_str = "#A< ( true and false ) #, ( 1==1 and 1==2 ) #, ( true and 1==2 ) #>"

source_ast = parser.parse(source_str)

print(source_ast)
print(CCLang.Lens.simplify(source_ast))


