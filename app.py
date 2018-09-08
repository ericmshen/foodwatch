import firebase_admin
from firebase_admin import db, credentials
from flask import *
from tempfile import mkdtemp
from twilio.rest import Client

app = Flask(__name__)

app.secret_key = 'ericbmi500'

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'


# Firebase Database
cred = credentials.Certificate('foodlord-5dd61-firebase-adminsdk-2ksfc-9d4371b135.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://foodlord-5dd61.firebaseio.com/'
    })

# Twilio
account_sid = 'ACa209e1ae289d60729d7321952c4d8974'
auth_token = '483d41d0e680edbfa018d0f0cfc6c578'

client = Client(account_sid, auth_token)

@app.route('/')
def index():
    foods = []
    for food in db.reference('items').get():
        foodData = db.reference('items/{0}'.format(food)).get()
        foods.append({
            'name': foodData['name'],
            'expiry': foodData['expiry']
            })
    message = client.messages.create(
        to="+14165539697",
        from_="+12672146320",
        body="u have the brain of a neanderthal")
    print(message.sid)
    return render_template('index.html', foods = foods)

if __name__ == '__main__':
    app.run(debug=True)
