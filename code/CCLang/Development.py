__author__ = 'Christoph Weygand <christophweygand@gmail.com>'

import CCLang.Parser
import CCLang.Lens

parser = CCLang.Parser.LEPLParser("#")
source = "#A< #B< 1 #, 2 #> #, #B< 3 #, 4 #> #>"
source_ast = parser.parse(source)

config = {"B": [0]}

updated_view = "#A<5 #, 6 #>"
view_ast = parser.parse(updated_view)

new_source_ast = CCLang.Lens.update(config, source_ast, view_ast, order=['A', 'B'])

print(new_source_ast)



