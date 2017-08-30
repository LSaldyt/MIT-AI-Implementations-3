from collections import defaultdict

class Instance(object):
    def __init__(self):
        self.json = defaultdict(dict)
        pass

    def __getitem__(self, key):
        return self.json[key]
