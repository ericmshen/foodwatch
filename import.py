import json
from pprint import pprint

with open('foodlord-5dd61-firebase-adminsdk-2ksfc-9d4371b135.json') as f:
    data = json.load(f)

pprint(data)

