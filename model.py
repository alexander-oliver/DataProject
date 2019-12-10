from login import LogIn
from labels import Labeler
from messages import Messenger
from hash import Hasher
import random

class Gmail:
    def __init__(self, credentials='credentials/credentials-CU.json'):
        self.service = LogIn(credentials)
        self.labels = Labeler(self.service)
        self.messages = Messenger(self.service)

    def hashMatch(self, labelNames, freq=.5, k=8, sample=50):
        messages = self.labels.match(labelNames)
        if sample and sample < len(messages):
            print(f'sampling {sample} messages of {len(messages)} matching {labelNames}')
            messages = random.sample(messages, sample)
        else:
            print(f'sampling {len(messages)} messages matching {labelNames}')
        return self.getHash(messages, freq=freq, k=k)

    def getHash(self, messages, freq=0.5, k=8):
        h = Hasher(k)
        for i,message in enumerate(messages):
            print(i, end='\r')
            content = self.messages.parseMessage(message)
            h.add(content)
        h.filter(freq)
        return h
