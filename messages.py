import base64
import re

def filter(m):
    filter_strings = [r'{[^}]*}', r'<[^>]*>', r'&nbsp;', r'&zwnj;', r'\n', r'\r', r'\t', r'\xa0']
    for f in filter_strings:
        m = re.sub(f,'',m)
    return m

class Messenger:
    def __init__(self, service):
        self.service = service
        self.next_page = None
        self.messages = None
        self.getMessages()

    def getMessages(self, reset=False):
        if (not self.next_page) or reset:
            results = self.service.users().messages().list(userId='me').execute()
        elif self.next_page == 'End':
            return None
        else:
            results = self.service.users().messages().list(userId='me', pageToken=self.next_page).execute()
        self.messages = results.get('messages',[])
        if 'nextPageToken' in results:
            self.next_page = results.get('nextPageToken',[])
        else:
            self.next_page = 'End'
        self.msg_idx = 0
        return True

    def currentMessage(self):
        if self.msg_idx < len(self.messages):
            return self.messages[self.msg_idx]
        else:
            if self.getMessages():
                return self.currentMessage()
            else:
                return 'No more messages'

    def nextMessage(self):
        self.msg_idx += 1
        return self.currentMessage()

    def readMessage(self, message=None):
        if not message:
            message = self.currentMessage()
        message = self.service.users().messages().get(userId='me', id=message['id']).execute()
        if 'parts' in message['payload']:
            parts = message['payload']['parts']
            out = ''
            for i in range(len(parts)):
                part = parts[i]
                body = part['body']
                if 'data' in body:
                    out += '\n'
                    out += base64.urlsafe_b64decode(body['data']).decode('utf-8')
                if 'parts' in part:
                    for i in range(len(part['parts'])):
                        b = part['parts'][i]['body']
                        if 'data' in b:
                            out += '\n'
                            out += base64.urlsafe_b64decode(b['data']).decode('utf-8')
        else:
            body = message['payload']['body']
            out = base64.urlsafe_b64decode(body['data']).decode('utf-8')
        return out

    def parseMessage(self, message=None):
        return filter(self.readMessage(message))

    def popMessage(self):
        out = self.currentMessage()
        self.nextMessage()
        return out
