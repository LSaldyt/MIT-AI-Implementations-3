import json
from collections import defaultdict, namedtuple
from itertools   import zip_longest
from pprint      import pprint

from utils import flatten

from variable_dictionary import VariableDictionary
from frame               import Frame

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

    def level_key_values(self, concept):
        def recursive_key_values(d):
            if isinstance(d, dict):
                # [[[..]]] potentially infinitely nested lists
                nested = [recursive_key_values(item) for item in d.values()]
                return [list(sorted(d.items(), key=lambda t:t[0]))] + [list(item) for item in zip(*flatten(nested))]
            else:
                return []
        return [[(concept, self.concepts[concept])]] + recursive_key_values(self.concepts[concept])

    def level_keys(self, concept):
        return [[k for k, v in kvs] for kvs in self.level_key_values(concept)]

    def level_values(self, concept):
        return [[v for k, v in kvs] for kvs in self.level_key_values(concept)]

    def compare_json_elements(self, variables, a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            json = dict()
            # recursive case
            for kA, vA in a.items():
                if kA in b:
                    vB = b[kA]
                    json[kA] = self.compare_json_elements(variables, vA, vB)
                else:
                    print('unmatched: ' + kA)
            for kB in b:
                if kB not in a:
                    print('unmatched: ' + kB)
        elif isinstance(a, list) and isinstance(b, list):
            # compare individual elements
            json = []
        else:
            # if unmatching or raw types, compare equal
            if a == b:
                json = a
            else:
                variables.add([a, b])
                json = variables.get_identifier()
        return json

    def create_frame(self, a, b):
        components = [a, b]
        variables  = VariableDictionary()
        aDict      = self.concepts[a]
        bDict      = self.concepts[b]
        json       = self.compare_json_elements(variables, aDict, bDict)

        return Frame(components, variables, json)
