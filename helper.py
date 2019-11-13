def getLabels(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    return labels

def getMessages(service):
    results = service.users().messages().list(userId='me').execute()
    message_ids = results.get('messages',[])
    return message_ids
