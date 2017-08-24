
class VariableDictionary(object):
    def __init__(self):
        self.variables  = dict()
        self.serial     = 0

    def __getitem__(self, key):
        return self.variables[key]

    def get_identifier(self):
        return '@{}'.format(self.serial)

    def add(self, value):
        self.serial += 1
        self.variables[self.get_identifier()] = value
