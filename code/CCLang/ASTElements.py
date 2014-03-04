__author__ = 'Waigie'

from lepl import List


class CCList(List):
    def choices(self):
        return []


class DimensionName(CCList):
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


class Alternative(CCList):
    def choices(self):
        return self[0].choices()


class Code(CCList):
    def choices(self):
        rtn = []
        for element in self:
            if isinstance(element, CCList):
                rtn += element.choices()
        return list(set(rtn))
