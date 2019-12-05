from model import Gmail
from shingles import *
G = Gmail()

labels = G.labels.getLabels()
labelId = {}
for label in labels:
    labelId[label['name']] = label['id']

# customLabels = ['Github', 'Ignore', 'Bills', 'SpamRecruiters', 'MARC', 'Cycling', 'Canvas', 'Piazza', 'Job Applications']

customLabels = ['Github', 'Canvas', 'Piazza', 'Ignore']


hash = {}
for label in customLabels:
    hash[label] = G.hash(labelId[label])
    print(len(hash[label]))

for i in range(100):
    message = G.messages.popMessage()
    content = G.messages.parseMessage(message)
    print('----\n\n')
    print(content[:100])
    mh, ms = None, 0
        for h in hash:
            s = QuickSim(shingles(8,content),hash[h])
            if s > ms:
                mh = h
                ms = s
        print(mh, ms)
