class Labeler:
    def __init__(self, service):
        self.service = service
        self.label_id = self.callLabelIds()

    def getLabelObjects(self, message=None):
        if message:
            message = self.service.users().messages().get(userId='me', id=message['id']).execute()
            return message['labelIds']
        else:
            results = self.service.users().labels().list(userId='me').execute()
            return results.get('labels',[])

    def setLabel(self, message, addLabelNames, rmLabelNames = []):
        body = { "addLabelIds": self.labelIds(addLabelNames),
                 "removeLabelIds" : self.labelIds(rmLabelNames)}
        message = self.service.users().messages().modify(userId='me', id=message['id'], body=body).execute()
        return message

    def createLabel(self, labelName):
        label = {'messageListVisibility':'show',
                'name':labelName,
                'labelListVisibility': 'labelShow'}
        label = self.service.users().labels().create(userId='me', body=label).execute()
        return label

    def callLabelIds(self):
        labels = self.getLabelObjects()
        ids = {}
        for label in labels:
            ids[label['name']] = label['id']
        return ids

    def names(self): return list(self.label_id.keys())

    def labelId(self, labelName):
        if labelName in self.label_id:
            return self.label_id[labelName]
        else:
            raise NameError(f'Label Name {labelName} does not exist.')

    def labelIds(self, labelNames): return [self.labelId(x) for x in labelNames]

    def match(self, labelNames):
        try:
            labelIds = self.labelIds(labelNames)
        except:
            self.label_id = self.callLabelIds()
            labelIds = self.labelIds(labelNames)
        response = self.service.users().messages().list(userId='me',
                                               labelIds=labelIds).execute()
        messages = []
        if 'messages' in response:
          messages.extend(response['messages'])

        while 'nextPageToken' in response:
          page_token = response['nextPageToken']
          response = self.service.users().messages().list(userId='me',
                                                     labelIds=labelIds,
                                                     pageToken=page_token).execute()
          messages.extend(response['messages'])

        return messages

    def clearLabel(self, match, labelIds):
        messages = self.listMessagesWithLabels(match)
        for m in messages:
            self.setLabel(m,labelIds,rm=True)
