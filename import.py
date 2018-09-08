import firebase_admin
from firebase_admin import db, credentials
from flask import *
from tempfile import mkdtemp
import json
from pprint import pprint
import csv
import pandas as pd
import datetime

# Firebase Database
cred = credentials.Certificate('foodlord-5dd61-firebase-adminsdk-2ksfc-9d4371b135.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://foodlord-5dd61.firebaseio.com/'
    })

with open('foodlord-5dd61-firebase-adminsdk-2ksfc-9d4371b135.json') as f:
    data = json.load(f)

data = json.loads(data)

file = csv.writer(open("food_expiry.csv", "wb+"))

def importdict(foodexpiry):
    df=pd.read_csv('foodlord-5dd61-firebase-adminsdk-2ksfc-9d4371b135' + '.csv'
    	information =['name', 'expiry']
    	sep = ';'
    	parse_dates=[0])
    fileDATES=df.T.to_dict().values()
    return fileDATES
if __name__ == '__main__':
    fileDATES = importdict('expiry')

data0=pd.read_csv('foodlord-5dd61-firebase-adminsdk-2ksfc-9d4371b135.json')

# %Y - year 
# %m - month (01 - 12)
# &d - day (01-31)
data0['expiry']=pd.to_datetime(data0['expiry'], format = "%Y/%m/%d")

now = datetime.datetime.now()

if "%d" - 7 == now:
	print("Your " + foodData['name'] + "expires in 1 week!")
	