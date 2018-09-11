import firebase_admin
from firebase_admin import db, credentials
from flask import *
from tempfile import mkdtemp
# from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = 'ericbmi500'

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'


# Firebase Database
cred = credentials.Certificate('<INSERT CERTIFICATE HERE>')
firebase_admin.initialize_app(cred, {
    'databaseURL': '<INSERT URL HERE>'
    })

time_between_insertion = datetime.now() - foodData['expiry']

if  time_between_insertion.days == 7:
    print "This item will expire in a week!"
