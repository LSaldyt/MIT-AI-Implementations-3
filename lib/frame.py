from pprint import pprint
from collections import defaultdict

class Frame(object):
    def __init__(self, components, variables, json):
        self.components = components
        self.variables  = variables
        self.json       = json

    def __str__(self):
        return str(self.json) + ', ' + str(self.variables.variables)

    def __repr__(self):
        return str(self)

    def gen_key(self):
        return '-'.join(sorted(self.components))
