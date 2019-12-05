from login import LogIn
from labels import Labeler
from messages import Messenger
from shingles import *
import random

class Gmail:
    def __init__(self, credentials='credentials/credentials-CU.json'):
        self.service = LogIn(credentials)
        self.labels = Labeler(self.service)
        self.messages = Messenger(self.service)

    def hash(self, LabelId, freq=.5, k=8):
        messages = self.labels.listMessagesWithLabels(LabelId)
        if len(messages) > 50:
            messages = random.sample(messages, 50)
        c = {}
        for message in messages:
            content = self.messages.parseMessage(message)
            c = addShingleCount(shingles(k,content),c)
        for x in list(c):
            if c[x] < freq*len(messages):
                del c[x]
        return set(c.keys())
