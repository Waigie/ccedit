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

    def pretty_print(self, choices, meta_marker):
        raise NotImplementedError

    def __eq__(self, other):
        choices_a = list(set(map(lambda x: (x.name(), x.alternative_count()), self.choices())))
        choices_b = list(set(map(lambda x: (x.name(), x.alternative_count()), other.choices())))
        if choices_a == choices_b:
            for config in configs(choices_a):
                if self.pretty_print(config, '#') != other.pretty_print(config, '#'):
                    return False
            return True
        else:
            return False


class DimensionName(CCList):
    def pretty_print(self, choices, meta_marker):
        return ' '+meta_marker+str(self)

    def __str__(self):
        return self[0]


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

    def pretty_print(self, choices, meta_marker):
        rtn = ''
        if self.name() in choices:
            choices[self.name()] = list(set(choices[self.name()]))
        if self.name() in choices and len(choices[self.name()]) == 1:
            if choices[self.name()][0] > self.alternative_count():
                raise ValueError
            rtn += self.alternatives()[choices[self.name()][0]].pretty_print(choices, meta_marker)
        elif self.name() in choices and len(choices[self.name()]) > 1:
            if max(choices[self.name()]) > self.alternative_count():
                raise ValueError
            rtn += meta_marker+self.name()+self.alternatives().pretty_print(
                choices,
                meta_marker,
                print_children=choices[self.name()]
            )
        else:
            rtn += meta_marker+self.name()+self.alternatives().pretty_print(
                choices,
                meta_marker,
                print_children=range(self.alternative_count())
            )
        return rtn

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

    def pretty_print(self, choices, meta_marker, print_children=[]):
        rtn = ''
        if len(print_children) == 1:
            pass
        else:
            children = (meta_marker+', ').join(
                map(
                    lambda y: y.pretty_print(choices, meta_marker),
                    map(lambda x: self[x], print_children))
            )
            rtn += ('< %s'+meta_marker+'> ') % children
        return rtn


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

    def pretty_print(self, choices, meta_marker):
        rtn = ''
        for element in self:
            if isinstance(element, CCList):
                rtn += element.pretty_print(choices, meta_marker)
            else:
                rtn += element+' '
        return rtn