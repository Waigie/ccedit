__author__ = 'Waigie'

from CCLang.ASTElements import *
import copy

def choice(config, oldast, newast, alt_counts=None):
    if alt_counts is None:
        alt_counts = {}
        for elm in oldast.choices():
            alt_counts[elm.name()] = elm.alternative_count()

    if len(config.keys()) == 0:
        return newast
    else:
        dim, sel = config.popitem()
        if len(sel) != 1:
            raise ValueError
        sel = sel[0]

        alternatives = Alternatives()

        for i in range(alt_counts[dim]):
            if i != sel:
                alternatives.append(oldast)
            else:
                alternatives.append(choice(config, oldast, newast, alt_counts))

        rtn = Code([Choice([dim, alternatives])])

        return rtn


def minimize(ast, selects={}):
    if isinstance(ast, Code):
        return Code(map(lambda elem: minimize(elem, selects), ast))
    elif isinstance(ast, Choice) and not (ast.name() in selects.keys()):
        alternatives = Alternatives()
        for i in range(ast.alternative_count()):
            tmp = copy.copy(selects);
            tmp[ast.name()] = i
            alternatives.append(minimize(ast.alternatives()[i], tmp))
        return Choice([ast.name(), alternatives])
    elif isinstance(ast, Choice) and ast.name() in selects.keys():
        selected = selects[ast.name()]
        return minimize(ast.alternatives()[selected], selects)
    else:
        return ast


simple_ast = Code([
    Choice([DimensionName(['A']),
            Alternatives([
                Alternative([Code(['1'])]),
                Alternative([Code(['2'])]),
            ])
    ])
])

newast = choice({'A': [1]}, simple_ast, Code(['3']))
print(newast.pretty_print({}, "#"))
newast = minimize(newast)

print(newast.pretty_print({}, "#"))

