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
        dim = sorted(config.keys())[0]
        sel = config.pop(dim)
        if len(sel) != 1:
            raise ValueError
        sel = sel[0]

        alternatives = Alternatives()

        for i in range(alt_counts[dim]):
            if i != sel:
                alternatives.append(Alternative([oldast]))
            else:
                alternatives.append(Alternative([choice(config, oldast, newast, alt_counts)]))

        rtn = Code([Choice([DimensionName([dim]), alternatives])])

        return rtn


def minimize(ast, selects={}):
    if isinstance(ast, Code):
        inner = list(map(lambda elem: minimize(elem, selects), ast))
        return Code(inner)
    elif isinstance(ast, Choice) and not (ast.name() in selects.keys()):
        alternatives = Alternatives()
        for i in range(ast.alternative_count()):
            tmp = copy.copy(selects)
            tmp[ast.name()] = i
            inner = minimize(ast.alternatives()[i], tmp)
            alternatives.append(inner)
        return Choice([DimensionName([ast.name()]), alternatives])
    elif isinstance(ast, Choice) and ast.name() in selects.keys():
        selected = selects[ast.name()]
        inner = minimize(ast.alternatives()[selected][0][0], selects)
        return inner
    elif isinstance(ast, Alternative):
        inner = minimize(ast[0], selects)
        rtn = Alternative()
        rtn.append(inner)
        return rtn
    else:
        return ast


def update(config, oldast, newast):
    return minimize(choice(config, oldast, newast))
