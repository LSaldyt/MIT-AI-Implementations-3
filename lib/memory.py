from collections import defaultdict

from .event import Event

class Memory(object):
    def __init__(self, initial):
        self.eventmap = defaultdict(set)
        self.initial  = initial
        self.time     = 0.0

    def __str__(self):
        return str(self.eventmap) + ', ' + str(self.initial)

    def add(self, event):
        self.eventmap[event.time].add(event)
        if event.time > self.time:
            self.time = event.time

    def act(self, keys, subchain, value):
        items = self.initial.select(keys)
        for item in items:
            keychain = tuple([item] + subchain)
            print(keychain)
            print(value)
            self.add(Event(keychain, value, self.time))
            self.time += 1
