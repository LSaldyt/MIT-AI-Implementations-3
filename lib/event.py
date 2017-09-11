class Event(object):

    def __init__(self, keychain, replacement, time):
        self.keychain    = keychain
        self.replacement = replacement
        self.time        = time
        self.original    = None

    def __str__(self):
        return ':'.join(self.keychain) + '->' + str(self.replacement) + '; t=' + str(self.time)

    def __repr__(self):
        return str(self)

    def apply(self, state):
        for key in keychain[:-1]:
            state = state[key]
        last = keychain[-1]
        if last in state:
            self.original = state[last]
        state[last] = replacement
