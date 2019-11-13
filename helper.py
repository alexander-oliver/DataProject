def getLabels(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    return labels

def getMessages(service):
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages',[])
    next_page = results.get('nextPageToken',[]) # TODO: Read next pages using a generator
    return messages # = list({'id', 'threadId'})

def readMessage(service, message):
    try:
        message = service.users().messages().get(userId='me', id=message['id']).execute()
        return message['snippet']
    except:
        return 'Error: Did not find message'
