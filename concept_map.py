import json
from collections import defaultdict, namedtuple

from utils import flatten

#from variable_dictionary import VariableDictionary

class ConceptMap(object):
    def __init__(self, filename):
        self.concepts = defaultdict(dict)
        with open(filename, 'r') as infile:
            self.concepts.update(json.load(infile))

    def __str__(self):
        return str(self.concepts)

    def shared_keys(self, *items):
        def get_keys (item):
            return set(self.concepts[item].keys())
        return set.intersection(*(get_keys(item) for item in items))

    def process_value(self, value):
        if isinstance(value, str):
            value = [value]
        elif isinstance(value, dict):
            raise NotImplementedError('Dictionary relations are more complex and not currently supported')
        return value

    def level_keys(self, concept):
        def recursive_keys(d):
            if isinstance(d, dict):
                # [[[..]]] potentially infinitely nested lists
                nested = [recursive_keys(item) for item in d.values()]
                return [list(d.keys())] + [list(item) for item in zip(*flatten(nested))]
            else:
                return []
        return [concept] + recursive_keys(self.concepts[concept])

