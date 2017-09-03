from collections import defaultdict

class Memory(object):
    def __init__(self, initial):
        self.eventmap = defaultdict(set)
        self.initial  = initial

    def __str__(self):
        return str(self.eventmap) + ', ' + str(self.initial)

    def add(self, event):
        self.eventmap[event.time].add(event)
