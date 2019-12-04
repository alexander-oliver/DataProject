from login import LogIn
from labels import Labeler
from messages import Messenger

class Gmail:
    def __init__(self, credentials='credentials/credentials-CU.json'):
        self.service = LogIn(credentials)
        self.labels = Labeler(self.service)
        self.messages = Messenger(self.service)
