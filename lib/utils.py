def flatten(l):
    return [item for sublist in l for item in sublist]

def chains(l):
    return [l[:i] for i in range(len(l))] + [l] + [l[i:] for i in range(1, len(l))]

