from login import LogIn

class Gmail:
    def __init__(self, credentials='credentials.json'):
        self.service = LogIn(credentials)
        self.messages = None
        self.msg_idx = None

    def getLabels(self):
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return labels

    def getMessages(self):
        results = self.service.users().messages().list(userId='me').execute()
        messages = results.get('messages',[])
        next_page = results.get('nextPageToken',[]) # TODO: Read next pages using a generator
        return messages # = list({'id', 'threadId'})

    def currentMessage(self):
        if not self.messages:
            self.messages = self.getMessages()
            self.msg_idx = 0
        if self.msg_idx < len(self.messages):
            return self.messages[self.msg_idx]
        else:
            # TODO: self.messages = next messages or empty
            self.msg_idx = 0
            return currentMessage

    def nextMessage(self):
        self.msg_idx += 1
        return self.currentMessage()

    def readMessage(self):
        try:
            message = self.currentMessage()
            print(message)
            message = self.service.users().messages().get(userId='me', id=message['id']).execute()
            return message['snippet']
        except:
            return 'Error: Did not find message'

G = Gmail()
print(G.readMessage())
G.nextMessage()
print(G.readMessage())
