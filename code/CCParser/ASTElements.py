__author__ = 'Waigie'

from lepl import List


class CCList(List):
    def choices(self):
        pass


class DimensionName(CCList):
    def __str__(self):
        return self[0]


class Choice(CCList):
    def name(self):
        return self[0]

    def alternatives(self):
        return self[0:]


class Alternatives(CCList):
    pass


class Alternative(CCList):
    pass


class Code(CCList):
    pass
