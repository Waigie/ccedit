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
        tmp = list(map(lambda elem: minimize(elem, selects), ast))
        inner = []
        for elem in tmp:
            if isinstance(elem, Code):
                for sub in elem:
                    inner.append(sub)
            else:
                inner.append(elem)
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
        inner = minimize(ast.alternatives()[selected], selects)
        return inner
    else:
        return ast


def eliminate_unused(ast):
    if isinstance(ast, Code):
        inner = list(map(lambda elem: eliminate_unused(elem), ast))
        return Code(inner)
    elif isinstance(ast, Choice):
        all_equiv = True
        for i in range(ast.alternative_count()):
            all_equiv &= ast.alternatives()[0].equiv(ast.alternatives()[i])
        if all_equiv:
            return eliminate_unused(ast.alternatives()[0])
        else:
            alternatives = Alternatives()
            for i in range(ast.alternative_count()):
                alternatives.append(eliminate_unused(ast.alternatives()[i]))
            return Choice([DimensionName([ast.name()]), alternatives])
    else:
        return ast


def simplify(ast):
    def find_in_ast(haystack, needle):
        for index, subast in enumerate(haystack):
            if subast == needle:
                return index
        return None

    if isinstance(ast, Code):
        rtn = Code([])
        inners = map(lambda elem: simplify(elem), ast)
        for inner in inners:
            if isinstance(inner, Code):
                for elem in inner:
                    rtn.append(elem)
            else:
                rtn.append(inner)
        return rtn
    elif isinstance(ast, Choice):
        simplified_alternatives = []
        for i in range(ast.alternative_count()):
            simplified_alternatives.append(simplify(ast.alternatives()[i]))

        for subast in simplified_alternatives[0]:
            references = []
            for alternative in simplified_alternatives:
                references.append(find_in_ast(alternative, subast))
            if None not in references:
                prefix_alternatives = []
                for index, reference in enumerate(references):
                    prefix_alternatives.append(Code(simplified_alternatives[index][0:reference]))
                prefix_choice = Choice([DimensionName([ast.name()]), Alternatives(prefix_alternatives)])

                suffix_alternatives = []
                for index, reference in enumerate(references):
                    suffix_alternatives.append(Code(simplified_alternatives[index][(reference+1):]))

                suffix_choice = Choice([DimensionName([ast.name()]), Alternatives(suffix_alternatives)])

                return simplify(eliminate_unused(Code([prefix_choice, simplified_alternatives[0][references[0]], suffix_choice])))

        return Choice([DimensionName([ast.name()]), simplified_alternatives])
    else:
        return ast


def update(config, oldast, newast):
    return eliminate_unused(minimize(choice(config, oldast, newast)))

