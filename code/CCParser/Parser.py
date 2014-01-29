__author__ = 'Christoph Weygand'

import re


class Parser:
    def __init__(self, input_data):
        self._input = input_data

    def parse(self):
        dimensions = self.find_dimensions()
        cleaned_text = self.remove_dimension_def()
        return Result(cleaned_text, dimensions)

    def find_dimensions(self):
        pattern = re.compile('dim (?P<name>\w+)<(?P<choices>[a-zA-Z0-9 _\-,]+)> in')
        dimensions = []
        for line in self._input.split("\n"):
            match = pattern.search(line)
            if match:
                name = match.groupdict().get('name')
                choices = [s.strip() for s in match.groupdict().get('choices').split(',')]
                dimensions.append((name, choices))
        return dimensions

    def remove_dimension_def(self):
        pattern = re.compile('dim (?P<name>\w+)<(?P<choices>[a-zA-Z0-9 _\-,]+)> in')
        result = ''
        for line in self._input.split("\n"):
            match = pattern.search(line)
            if not match:
                result += line + "\n"
        return result



class Result:
    def __init__(self, text, dimensions):
        self._text = text
        self._dimensions = dimensions

    def get_text(self):
        return self._text

    def get_dimensions(self):
        return self._dimensions