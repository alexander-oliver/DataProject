import random

def shingles(k, s):
    return set([s[i:i+k] for i in range(len(s)-k)])

# Hashers are baskets of common k-shingles
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

    def countFilter(self, freq):
        tol = freq * self.n
        i = 0
        for x in self.count:
            if self.count[x] >= tol:
                i += 1
        return i

    def showFilter(self, freq):
        tol = freq * self.n
        show = {}
        for x in self.count:
            if self.count[x] >= tol:
                show[x] = self.count[x]
        return show

    def add(self, message):
        self.n += 1
        s = shingles(self.k, message)
        for x in s:
            if x in self.count:
                self.count[x] += 1
            else:
                self.count[x] = 1

    def sim(self, message, freq):
        s = shingles(self.k, message)
        tol = freq * self.n
        i = 0
        n = 0
        for x in self.count:
            if self.count[x] > tol:
                n += 1
                if x in s:
                    i += 1
        return i/n
