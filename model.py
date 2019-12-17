from login import LogIn
from labels import Labeler
from messages import Messenger

class Gmail:
    def __init__(self, credentials='credentials/credentials-CU.json'):
        self.service = LogIn(credentials)
        self.labels = Labeler(self.service)
        self.messages = Messenger(self.service)

    def get(self, labelName):
        return self.labels.match([labelName])

    def parse(self, message):
        return self.messages.parseMessage(message)

    def setLabel(self, message, label):
        self.labels.setLabel(message, [label])
