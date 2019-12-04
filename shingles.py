def shingles(k, s):
    return set([s[i:i+k] for i in range(len(s)-k)])

def JaccardSim(x,y):
    return len(x.intersection(y))/len(x.union(y))

def addShingleCount(s, counts={}):
    for x in s:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

def similarity(shin, count):
    i = 0
    for x in shin:
        if x in count:
            i += count[x]
    j = 0
    for x in count:
        j += count[x]
    return i/j
