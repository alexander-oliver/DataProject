def shingles(k, s):
    return set([s[i:i+k] for i in range(len(s)-k)])

def addShingleCount(s, counts={}):
    for x in s:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

def JaccardSim(x,y):
    return len(x.intersection(y))/len(x.union(y))

def QuickSim(sample, hash):
    return len(sample.intersection(hash))/len(hash)
