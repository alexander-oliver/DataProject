from login import LogIn
import base64
import re

class Gmail:
    def __init__(self, credentials='credentials-CU.json'):
        self.service = LogIn(credentials)
        self.getMessages()

    def getMessages(self, reset=False):
        self.msg_idx = 0
        if not hasattr(self, 'next_page'):
            self.next_page = None
        if (not reset) and self.next_page=='End': # No more messages left
            return None
        if (not self.next_page) or reset: # Get first page of messages
            results = self.service.users().messages().list(userId='me').execute()
            self.messages = results.get('messages',[])
            self.next_page = results.get('nextPageToken',[])
        else: # Get next page of messages
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
            if self.getMessages(): return self.currentMessage()
            else: return 'No more messages'

    def nextMessage(self):
        self.msg_idx += 1
        return self.currentMessage()

    def readMessage(self, message=None):
        try:
            if not message:
                message = self.currentMessage()
            message = self.service.users().messages().get(userId='me', id=message['id']).execute()
            if 'parts' in message['payload']:
                parts = message['payload']['parts']
                out = ''
                for i in range(len(parts)):
                    body = parts[i]['body']
                    if 'data' in body:
                        out += '\n\n\n\n'
                        out += base64.urlsafe_b64decode(body['data']).decode('utf-8')
            else:
                body = message['payload']['body']
                out = base64.urlsafe_b64decode(body['data']).decode('utf-8')

            return out
        except:
            print('error with', message)
            return 'error reading message'

    def filter(self, m):
        filter_strings = [r'{[^}]*}', r'<[^>]*>', r'&nbsp;', r'&zwnj;', r'\n', r'\r', r'\t', r'\xa0']
        for f in filter_strings:
            m = re.sub(f,'',m)
        return m

    def parseMessage(self, message=None):
        return self.filter(self.readMessage(message))

    def popMessage(self):
        out = self.parseMessage()
        self.nextMessage()
        return out

    # #
    # Labeling Functions
    # #

    # Returns a list of all labels if a message is not given
    def getLabels(self, message=None):
        if message:
            message = self.service.users().messages().get(userId='me', id=message['id']).execute()
            return message['labelIds']
        else:
            results = self.service.users().labels().list(userId='me').execute()
            return results.get('labels',[])

    def setLabel(self, message, label, rm=False):
        try:
            if not rm:
                body = { "addLabelIds": [label['id']]}
            else:
                body = {"removeLabelIds" : [label['id']]}
            message = self.service.users().messages().modify(userId='me', id=message['id'], body=body).execute()
            return message
        except:
            return 'error setting label'

    def createLabel(self, labelName):
        label = {'messageListVisibility':'show',
                'name':labelName,
                'labelListVisibility': 'labelShow'}
        try:
            label = self.service.users().labels().create(userId='me', body=label).execute()
            print(label)
            return label
        except:
            return 'error creating label'

    def listMessagesWithLabels(self, label_ids=[]):
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
            return 'error listing messages with labels'
