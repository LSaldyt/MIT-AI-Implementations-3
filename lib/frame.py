from pprint import pprint
from collections import defaultdict

class Frame(object):
    def __init__(self, components, variables, json):
        self.components = components
        self.variables  = variables
        self.json       = json

    def show(self):
        pprint(self.json)
        pprint(self.variables.variables)

    def gen_key(self):
        return '-'.join(sorted(self.components))
