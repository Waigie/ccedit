__author__ = 'Waigie'

from CCLang.ASTElements import *
import copy

def choice(config, oldast, newast, alt_counts=None):
    if alt_counts is None:
        alt_counts = {}
        for elm in oldast.dims():
            alt_counts[elm.name()] = elm.alternative_count()
        for elem in newast.dims():
            if not (elem.name() in alt_counts):
                alt_counts[elem.name()] = elem.alternative_count()
            elif alt_counts[elem.name()] < elem.alternative_count():
                alt_counts[elem.name()] = elem.alternative_count()

    for k in config.keys():
        alt_counts[k] = max(alt_counts.get(k,  0), 2)

    if len(config.keys()) == 0:
        return newast
    else:
        dim = sorted(config.keys())[0]
        sel = config.pop(dim)
        if len(sel) != 1:
            raise ValueError
        sel = sel[0]

        alternatives = Alternatives()

        for i in range(alt_counts.get(dim, 0)):
            if i != sel:
                alternatives.append(oldast)
            else:
                alternatives.append(choice(config, oldast, newast, alt_counts))

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
        inner = minimize(ast.alternatives()[selected][0], selects)
        return inner
    else:
        return ast


def update(config, oldast, newast):
    return minimize(choice(config, oldast, newast))

