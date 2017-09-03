from collections import defaultdict

class Instance(object):
    def __init__(self, setName, setJson=None):
        if setJson is None:
            setJson = dict()
        self.name = setName
        self.json = setJson

    def __getitem__(self, key):
        return self.json[key]

    def __str__(self):
        return self.name + ', ' + str(self.json)

    def __repr__(self):
        return str(self)
