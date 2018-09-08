import json
from pprint import pprint
import csv
import pandas as pd

with open('foodlord-5dd61-firebase-adminsdk-2ksfc-9d4371b135.json') as f:
    data = json.load(f)

pprint(data)

data = json.loads(data)

file = csv.writer(open("food_expiry.csv", "wb+"))

def importdict('food expiry.csv'):
    df=pd.read_csv(filename+'.csv', names=['systemtime', 'Var1', 'var2'],sep=';',parse_dates=[0])
    fileDATES=df.T.to_dict().values()
    return fileDATES
if __name__ == '__main__':
    fileDATES = importdict('dates')

