import random

def shingles(k, s):
    return set([s[i:i+k] for i in range(len(s)-k)])

class Hasher:
    def __init__(self, k):
        self.count = {}
        self.k = k
        self.n = 0

    def __call__(self):
        return set(self.count.keys())

    def __len__(self):
        return len(self.count)

    def __repr__(self):
        return self().__repr__()

    def filter(self, freq):
        for x in list(self.count):
            if self.count[x] < self.n * freq:
                del self.count[x]

    def add(self, message):
        self.n += 1
        s = shingles(self.k, message)
        for x in s:
            if x in self.count:
                self.count[x] += 1
            else:
                self.count[x] = 1

    def sim(self, message):
        s = shingles(self.k, message)
        i = 0
        for x in s:
            if x in self.count:
                i += 1
        return i/len(self.count)
