from login import LogIn
from helper import *

service = LogIn()
print([x['name'] for x in getLabels(service)])

messages = getMessages(service)
for m in messages[:5]:
    print(m)
    print(readMessage(service,m))
