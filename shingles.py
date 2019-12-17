import random

def shingles(k, s):
    return set([s[i:i+k] for i in range(len(s)-k)])

# Hashers are baskets of common k-shingles
class Shingler:
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
            if self.count[x] >= tol:
                n += 1
                if x in s:
                    i += 1
        return i/(n+1)

class nShingles:
    def __init__(self, k=8, n=3):
        self.S = {}
        for i in range(n):
            H = Shingler(k)
            self.S[i] = H

    def size(self):
        L = {}
        for x in self.S:
            L[x] = len(self.S[x])
        return L

    def n(self):
        L = {}
        for x in self.S:
            L[x] = self.S[x].n
        return L

    def groups(self):
        return list(self.S.keys())

    def name(self, group, name):
        if group in self.S:
            self.S[name] = self.S[group]
            del self.S[group]
        else:
            raise NameError('group does not exist')

    def add(self, content, freq=.5):
        mx, ms = -1,-1
        for x in self.S:
            if self.S[x].n == 0:
                ms = 1
                mx = x
                break
            s = self.S[x].sim(content, freq)
            if s > ms:
                ms = s
                mx = x
        self.S[mx].add(content)
        return (mx, ms)

    def ins(self, content, group):
        if group in self.S:
            self.S[group].add(content)
        else:
            raise NameError('group does not exist')

    def sim(self, content, freq=.5):
        mx, ms = -1,-1
        for x in self.S:
            s = self.S[x].sim(content, freq)
            if s > ms:
                ms = s
                mx = x
        return (mx, ms)

    def filter(self, freq = 0.1):
        for x in self.S:
            self.S[x].filter(freq)
