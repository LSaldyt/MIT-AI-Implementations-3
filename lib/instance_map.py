import json
from collections import defaultdict, namedtuple
from itertools   import zip_longest
from pprint      import pprint

from .utils import flatten

from .variable_dictionary import VariableDictionary
from .frame               import Frame

class InstanceMap(object):
    def __init__(self, filename):
        self.instances = defaultdict(dict)
        with open(filename, 'r') as infile:
            self.instances.update(json.load(infile))
        self.map = defaultdict(set)

    def __str__(self):
        return str(self.instances)

    def shared_keys(self, *items):
        def get_keys (item):
            return set(self.instances[item].keys())
        return set.intersection(*(get_keys(item) for item in items))

    def process_value(self, value):
        if isinstance(value, str):
            value = [value]
        elif isinstance(value, dict):
            raise NotImplementedError('Dictionary relations are more complex and not currently supported')
        return value

    def level_keychains(self, instance):
        def recursive_keychain(d):
            if isinstance(d, dict):
                return [[[k, *nested] for nested in flatten(recursive_keychain(v))] if isinstance(v, dict) else [[k]] 
                        for k, v in d.items()]
            else:
                return []
        return recursive_keychain(self.instances[instance])

    def level_key_values(self, instance):
        def recursive_key_values(d):
            if isinstance(d, dict):
                # [[[..]]] potentially infinitely nested lists
                nested = [recursive_key_values(item) for item in d.values()]
                return [list(sorted(d.items(), key=lambda t:t[0]))] + [list(item) for item in zip(*flatten(nested))]
            else:
                return []
        return [[(instance, self.instances[instance])]] + recursive_key_values(self.instances[instance])

    def level_keys(self, instance):
        return [[k for k, v in kvs] for kvs in self.level_key_values(instance)]

    def level_values(self, instance):
        return [[v for k, v in kvs] for kvs in self.level_key_values(instance)]

    def update_item(self, item):
        for keychains in self.level_keychains(item):
            for keychain in keychains:
                value = self.instances[item]
                for key in keychain:
                    value = value[key]
                self.map[value].add((item,) + tuple(keychain))

    def update_map(self):
        for item in self.instances:
            self.update_item(item)

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
        print('Creating frame between objects {} and {}:'.format(a, b))
        components = [a, b]
        variables  = VariableDictionary()
        aDict      = self.instances[a]
        bDict      = self.instances[b]
        json       = self.compare_json_elements(variables, aDict, bDict)

        return Frame(components, variables, json)
