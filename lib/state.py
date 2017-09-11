import json
from collections import defaultdict, namedtuple
from itertools   import zip_longest
from pprint      import pprint

from .utils import flatten, chains

from .variable_dictionary import VariableDictionary
from .frame               import Frame
from .instance            import Instance

class State(object):
    def __init__(self, filename):
        self.instances = defaultdict(dict)
        with open(filename, 'r') as infile:
            instances = json.load(infile)
            for k, v in instances.items():
                instances[k] = Instance(k, v)

            self.instances.update(instances)
        self.map = defaultdict(set)
        self.keymap = defaultdict(set)

    def __str__(self):
        return str(self.instances)

    def add(self, name, instance):
        self.instances[name] = instance

    def _subchains(self, k, v):
        if isinstance(v, dict):
            return [[k, *chain] for nested in flatten(self.recursive_keychain(v)) for chain in chains(nested)]
        else:
            return [[k]] 

    def recursive_keychain(self, d):
        isInstance = isinstance(d, Instance)
        isDict     = isinstance(d, dict)
        if isInstance or isDict:
            if isInstance:
                d = d.json
            return [self._subchains(k, v) for k, v in d.items()]
        else:
            return []

    def level_keychains(self, instance):
        return self.recursive_keychain(self.instances[instance])

    def update_item(self, item):
        for keychains in self.level_keychains(item):
            for keychain in keychains:
                value = self.instances[item]
                for key in keychain:
                    value = value[key]
                for i, key in enumerate(keychain):
                    self.keymap[key].add((tuple([item] + keychain), i+1))
                if isinstance(value, list):
                    value = tuple(sorted(value))
                if isinstance(value, dict) or isinstance(value, defaultdict):
                    value = tuple(sorted(value.items()))
                keychain = [item] + keychain

                for i in range(len(keychain)):
                    if i != 0:
                        self.map[tuple(keychain[i:] + [value])].add(tuple(keychain))
                self.map[value].add(tuple(keychain))

    def update_map(self):
        for item in self.instances:
            self.update_item(item)

    def compare_json_elements(self, variables, a, b):
        aIsInstance = isinstance(a, Instance)
        bIsInstance = isinstance(b, Instance)
        aIsDict = isinstance(a, dict)
        bIsDict = isinstance(b, dict)
        if (aIsDict and bIsDict) or (aIsInstance and bIsInstance):
            if aIsInstance:
                a = a.json
                b = b.json
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
        print('Creating frame between objects {} and {}:'.format(a, b))
        components = [a, b]
        variables  = VariableDictionary()
        aDict      = self.instances[a]
        bDict      = self.instances[b]
        json       = self.compare_json_elements(variables, aDict, bDict)

        return Frame(components, variables, json)
