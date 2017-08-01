
class VariableDictionary(object):
    def __init__(self):
        self.variables  = dict()
        self.serial     = 0

    def get_identifier(self):
        return '@{}'.format(self.serial)

    def add(self, value):
        self.variables[self.get_identifier()] = value
        self.serial += 1
