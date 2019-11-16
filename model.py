from login import LogIn
import base64
import re

class Gmail:
    def __init__(self, credentials='credentials.json'):
        self.service = LogIn(credentials)
        self.next_page = None
        self.messages = self.getMessages()
        self.msg_idx = 0

    def getLabels(self):
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return labels

    def getMessages(self, reset=False):
        if (not reset) and self.next_page=='End':
            return None
        if (not self.next_page) or reset:
            results = self.service.users().messages().list(userId='me').execute()
            self.messages = results.get('messages',[])
            self.next_page = results.get('nextPageToken',[])
        else:
            results = self.service.users().messages().list(userId='me', pageToken=self.next_page).execute()
            self.messages = results.get('messages',[])
            if 'nextPageToken' in results:
                self.next_page = results.get('nextPageToken',[])
            else:
                self.next_page = 'End'
                return False
        return True

    def currentMessage(self):
        if self.msg_idx < len(self.messages):
            return self.messages[self.msg_idx]
        else:
            # TODO: self.messages = next messages or empty
            self.msg_idx = 0
            if self.getMessages():
                return currentMessage()
            else:
                return 'No more messages'

    def nextMessage(self):
        self.msg_idx += 1
        return self.currentMessage()

    def readMessage(self):
        try:
            message = self.currentMessage()
            message = self.service.users().messages().get(userId='me', id=message['id']).execute()
            if 'parts' in message['payload']:
                parts = message['payload']['parts']
                out = ''
                for i in range(len(parts)):
                    body = parts[i]['body']
                    out += '\n\n\n\n'
                    out += base64.urlsafe_b64decode(body['data']).decode('utf-8')
            else:
                body = message['payload']['body']
                out = base64.urlsafe_b64decode(body['data']).decode('utf-8')

            return out
        except:
            return 'failed'

    def filter(self, m):
        filter_strings = [r'{[^}]*}', r'<[^>]*>', r'&nbsp;', r'&zwnj;', r'\n', r'\r', r'\t', r'\xa0']
        for f in filter_strings:
            m = re.sub(f,'',m)
        return m

    def parseMessage(self):
        return self.filter(self.readMessage())

    def popMessage(self):
        out = self.parseMessage()
        self.nextMessage()
        return out
