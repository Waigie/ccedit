__author__ = 'Waigie'

from lepl import List


def configs(dims):
    if dims:
        current = dims.pop()
        rtn = []
        for config in configs(dims):
            for i in range(current[1]):
                tmp = config.copy()
                tmp[current[0]] = [i]
                rtn.append(tmp)
        return rtn
    else:
        return [{}]


class CCList(List):
    def dims(self):
        raise NotImplementedError

    def pretty_print(self, meta_marker):
        raise NotImplementedError

    def apply_config(self, config):
        raise NotImplementedError

    def apply_and_print(self, config, meta_marker):
        return self.apply_config(config).pretty_print(meta_marker)

    def equiv(self, other):
        dims_a = list(set(map(lambda x: (x.name(), x.alternative_count()), self.dims())))
        dims_b = list(set(map(lambda x: (x.name(), x.alternative_count()), other.dims())))
        dims = list(set(dims_a + dims_b))
        # if choices_a == choices_b:
        for config in configs(dims):
            if self.apply_config(config) != other.apply_config(config):
                return False
        return True
        # else:
        #     return False


class DimensionName(CCList):
    def pretty_print(self, meta_marker):
        return ' '+meta_marker+str(self)

    def apply_config(self, choices):
        return self

    def __str__(self):
        return self[0]

    def apply_and_print(self, config, meta_marker):
        return self.apply_config(config).pretty_print(meta_marker)


class Choice(CCList):
    def name(self):
        return self[0][0]

    def alternatives(self):
        return self[1]

    def alternative_count(self):
        return len(self[1])

    def dims(self):
        rtn = [self]
        rtn += self.alternatives().dims()
        return rtn

    def apply_config(self, config):
        if self.name() in config:
            config[self.name()] = list(set(config[self.name()]))

        if self.name() in config and len(config[self.name()]) == 1:
            if config[self.name()][0] > self.alternative_count():
                raise ValueError
            return self.alternatives()[config[self.name()][0]].apply_config(config)
        if self.name() in config and len(config[self.name()]) > 1:
            alternatives = Alternatives()
            for i in config[self.name()]:
                alternatives.append(self.alternatives()[i].apply_config(config))
            return Choice([self[0], alternatives])
        else:
            alternatives = Alternatives()
            for i in range(self.alternative_count()):
                alternatives.append(self.alternatives()[i].apply_config(config))
            return Choice([self[0], alternatives])

    def pretty_print(self, meta_marker):
        rtn = ''
        rtn += meta_marker+self.name()+self.alternatives().pretty_print(
            meta_marker,
            print_children=range(self.alternative_count())
        )
        return rtn

    def apply_and_print(self, config, meta_marker):
        return self.apply_config(config).pretty_print(meta_marker)

    def __hash__(self):
        return hash(self.name())

    def __str__(self):
        return self.name()


class Alternatives(CCList):
    def dims(self):
        rtn = []
        for element in map(lambda alternative: alternative.dims(), self):
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

    def apply_config(self, config):
        return self

    def apply_and_print(self, config, meta_marker):
        return self.apply_config(config).pretty_print(meta_marker)


# class Alternative(CCList):
#     def choices(self):
#         return self[0].choices()
#
#     def pretty_print(self, choices, meta_marker):
#         return self[0].pretty_print(choices, meta_marker)


class Code(CCList):
    def dims(self):
        rtn = []
        for element in self:
            if isinstance(element, CCList):
                rtn += element.dims()
        return list(set(rtn))

    def pretty_print(self, meta_marker):
        rtn = ''
        for element in self:
            if isinstance(element, CCList):
                rtn += element.pretty_print(meta_marker)
            else:
                rtn += element+' '
        return rtn

    def apply_config(self, config):
        configured_children = []
        for child in self:
            if isinstance(child, CCList):
                configured_children.append(child.apply_config(config))
            else:
                configured_children.append(child)

        ## remove code -> code tree structure

        for i in range(len(configured_children)):
            if isinstance(configured_children[i], Code):
                elem = configured_children.pop(i)
                for child in reversed(elem):
                    configured_children.insert(i, child)

        return Code(configured_children)

    def apply_and_print(self, config, meta_marker):
        return self.apply_config(config).pretty_print(meta_marker)