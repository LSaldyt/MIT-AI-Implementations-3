from collections import defaultdict

class FrameMap(object):
    def __init__(self):
        self.componentmap = defaultdict(set)
        self.map = dict()

    def add(self, frame):
        key = frame.gen_key()
        for component in frame.components:
            self.componentmap[component].add(key)
        self.map[key] = frame

    def get(self, key):
        return self.map[key]

    def get_all(self, component):
        keys = self.componentmap[component]
        return [self.get(key) for key in keys]
