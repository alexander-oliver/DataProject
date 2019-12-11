class Labeler:
    def __init__(self, service):
        self.service = service
        self.label_id = self.callLabelIds()

    def getLabel(self, message=None):
        if message:
            message = self.service.users().messages().get(userId='me', id=message['id']).execute()
            return self.labelNames(message['labelIds'])
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
        labels = self.getLabel()
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

    def labelName(self, labelId):
        for labelName in self.label_id:
            if self.label_id[labelName] == labelId:
                return labelName
        raise NameError(f'Label Id {labelId} does not exist')

    def labelNames(self, labelIds): return [self.labelName(x) for x in labelIds]

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
          if 'messages' in response:
            messages.extend(response['messages'])

        return messages

    def clearLabel(self, match, rmLabelNames, addLabelNames=None):
        messages = self.match(match)
        for m in messages:
            self.setLabel(m,addLabelNames,rmLabelNames)
