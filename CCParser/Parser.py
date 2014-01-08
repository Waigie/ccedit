__author__ = 'Christoph Weygand'

import re

class Parser:
    def __init__(self, input_data):
        self.input = input_data

    def parse(self):
        dimensions = self.find_dimensions()
        for dimension in dimensions:
            print(dimension)

    def find_dimensions(self):
        pattern = re.compile('dim (?P<name>\w+)<(?P<choices>[a-zA-Z0-9 _\-,]+)> in')
        dimensions = []
        for line in self.input.split("\n"):
            match = pattern.search(line)
            if match:
                name = match.groupdict().get('name')
                choices = [s.strip() for s in match.groupdict().get('choices').split(',')]
                dimensions.append((name, choices))
        return dimensions

