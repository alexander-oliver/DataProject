from login import LogIn
import base64
import re

class Gmail:
    def __init__(self, credentials='credentials.json'):
        self.service = LogIn(credentials)
        self.next_page = None
        self.getMessages()
        self.msg_idx = 0

    def getLabels(self, msgId=None):
        if msgId:
            message = self.service.users().messages().get(userId='me', id=msgId).execute()
            return message['labelIds']
        else:
            results = self.service.users().labels().list(userId='me').execute()
        return results.get('labels',[])

    def setLabel(self, msgId, label, add=True):
        try:
            print(label['id'])
            if add:
                body = { "addLabelIds": [label['id']],
                "removeLabelIds" : []}
            else:
                print('here')
                body = {"addLabelIds": [],
                "removeLabelIds" : [label['id']]}
            print(body)
            message = self.service.users().messages().modify(userId='me', id=msgId, body=body).execute()
            return message
        except:
            return 'error'

    def ListMessagesWithLabels(self, label_ids=[]):
        try:
            response = self.service.users().messages().list(userId='me',
                                                   labelIds=label_ids).execute()
            messages = []
            if 'messages' in response:
              messages.extend(response['messages'])

            while 'nextPageToken' in response:
              page_token = response['nextPageToken']
              response = self.service.users().messages().list(userId='me',
                                                         labelIds=label_ids,
                                                         pageToken=page_token).execute()
              messages.extend(response['messages'])

            return messages
        except:
            return 'error'

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
