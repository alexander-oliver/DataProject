from login import LogIn
from helper import *

service = LogIn()
print([x['name'] for x in getLabels(service)])
