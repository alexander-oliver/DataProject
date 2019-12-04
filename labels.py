class Labeler:
    def __init__(self, service):
        self.service = service

    # Returns a list of all labels if a message is not given
    def getLabels(self, message=None):
        if message:
            message = self.service.users().messages().get(userId='me', id=message['id']).execute()
            return message['labelIds']
        else:
            results = self.service.users().labels().list(userId='me').execute()
            return results.get('labels',[])

    def setLabel(self, message, label, rm=False):
        if not rm:
            body = { "addLabelIds": [label['id']]}
        else:
            body = {"removeLabelIds" : [label['id']]}
        message = self.service.users().messages().modify(userId='me', id=message['id'], body=body).execute()
        return message

    def createLabel(self, labelName):
        label = {'messageListVisibility':'show',
                'name':labelName,
                'labelListVisibility': 'labelShow'}
        label = self.service.users().labels().create(userId='me', body=label).execute()
        print(label)
        return label

    def listMessagesWithLabels(self, label_ids):
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
