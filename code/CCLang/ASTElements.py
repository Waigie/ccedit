__author__ = 'Waigie'

from lepl import List


def configs(choices):
    if choices:
        current = choices.pop()
        rtn = []
        for config in configs(choices):
            for i in range(current[1]):
                tmp = config.copy()
                tmp[current[0]] = [i]
                rtn.append(tmp)
        return rtn
    else:
        return [{}]


class CCList(List):
    def choices(self):
        raise NotImplementedError

    def pretty_print(self, meta_marker):
        raise NotImplementedError

    def apply_config(self, choices):
        raise NotImplementedError

    def apply_and_print(self, choices, meta_marker):
        return self.apply_config(choices).pretty_print(meta_marker)

    def equiv(self, other):
        choices_a = list(set(map(lambda x: (x.name(), x.alternative_count()), self.choices())))
        choices_b = list(set(map(lambda x: (x.name(), x.alternative_count()), other.choices())))
        if choices_a == choices_b:
            for config in configs(choices_a):
                if self.apply_config(config) != other.apply_config(config):
                    return False
            return True
        else:
            return False


class DimensionName(CCList):
    def pretty_print(self, meta_marker):
        return ' '+meta_marker+str(self)

    def apply_config(self, choices):
        return self

    def __str__(self):
        return self[0]

    def apply_and_print(self, choices, meta_marker):
        return self.apply_config(choices).pretty_print(meta_marker)


class Choice(CCList):
    def name(self):
        return self[0][0]

    def alternatives(self):
        return self[1]

    def alternative_count(self):
        return len(self[1])

    def choices(self):
        rtn = [self]
        rtn += self.alternatives().choices()
        return rtn

    def apply_config(self, choices):
        if self.name() in choices:
            choices[self.name()] = list(set(choices[self.name()]))

        if self.name() in choices and len(choices[self.name()]) == 1:
            if choices[self.name()][0] > self.alternative_count():
                raise ValueError
            return self.alternatives()[choices[self.name()][0]].apply_config(choices)
        if self.name() in choices and len(choices[self.name()]) > 1:
            alternatives = Alternatives()
            for i in choices[self.name()]:
                alternatives.append(self.alternatives()[i].apply_config(choices))
            return Choice([self[0], alternatives])
        else:
            alternatives = Alternatives()
            for i in range(self.alternative_count()):
                alternatives.append(self.alternatives()[i].apply_config(choices))
            return Choice([self[0], alternatives])

    def pretty_print(self, meta_marker):
        rtn = ''
        rtn += meta_marker+self.name()+self.alternatives().pretty_print(
            meta_marker,
            print_children=range(self.alternative_count())
        )
        return rtn

    def apply_and_print(self, choices, meta_marker):
        return self.apply_config(choices).pretty_print(meta_marker)

    def __hash__(self):
        return hash(self.name())

    def __str__(self):
        return self.name()


class Alternatives(CCList):
    def choices(self):
        rtn = []
        for element in map(lambda alternative: alternative.choices(), self):
            rtn += element
        return rtn

    def pretty_print(self, meta_marker, print_children=[]):
        rtn = ''
        if len(print_children) == 1:
            pass
        else:
            children = (meta_marker+', ').join(
                map(
                    lambda y: y.pretty_print(meta_marker),
                    map(lambda x: self[x], print_children))
            )
            rtn += ('< %s'+meta_marker+'> ') % children
        return rtn

    def apply_config(self, choices):
        return self

    def apply_and_print(self, choices, meta_marker):
        return self.apply_config(choices).pretty_print(meta_marker)


# class Alternative(CCList):
#     def choices(self):
#         return self[0].choices()
#
#     def pretty_print(self, choices, meta_marker):
#         return self[0].pretty_print(choices, meta_marker)


class Code(CCList):
    def choices(self):
        rtn = []
        for element in self:
            if isinstance(element, CCList):
                rtn += element.choices()
        return list(set(rtn))

    def pretty_print(self, meta_marker):
        rtn = ''
        for element in self:
            if isinstance(element, CCList):
                rtn += element.pretty_print(meta_marker)
            else:
                rtn += element+' '
        return rtn

    def apply_config(self, choices):
        configured_children = []
        for child in self:
            if isinstance(child, CCList):
                configured_children.append(child.apply_config(choices))
            else:
                configured_children.append(child)

        ## remove code -> code tree structure

        for i in range(len(configured_children)):
            if isinstance(configured_children[i], Code):
                elem = configured_children.pop(i)
                for child in elem:
                    configured_children.insert(i, child)

        return Code(configured_children)

    def apply_and_print(self, choices, meta_marker):
        return self.apply_config(choices).pretty_print(meta_marker)