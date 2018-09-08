import json
from pprint import pprint

with open('foodlordgoogle.json') as f:
    data = json.load(f)

pprint(data)