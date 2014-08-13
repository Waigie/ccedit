import CCLang.Parser
import CCLang.Lens

parser = CCLang.Parser.LEPLParser("#")
#source_str = "#A< ( true and false ) #, ( 1==1 and 1==2 ) #, ( true and 1==2 ) #>"
source_str = "#A< g( 1 ) #, 2 #>";
updated_view = "g( 2 )"

source_ast = parser.parse(source_str)
view_ast = parser.parse(updated_view)

print(source_ast)
print(view_ast)

new_ast = CCLang.Lens.update({"A": [1]}, source_ast, view_ast)
print(new_ast)
print(CCLang.Lens.minimize(new_ast))
#print(CCLang.Lens.simplify(source_ast))


