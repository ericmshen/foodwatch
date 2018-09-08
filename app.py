import firebase_admin, datetime
from firebase_admin import db, credentials
from flask import *
from tempfile import mkdtemp
# from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from datetime import timedelta, date, datetime

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

root = db.reference()

# Twilio
account_sid = 'ACa209e1ae289d60729d7321952c4d8974'
auth_token = '483d41d0e680edbfa018d0f0cfc6c578'

client = Client(account_sid, auth_token)


@app.route("/sms", methods=['GET', 'POST'])
def sms():
    """Respond to incoming messages with a friendly SMS."""

    requested = request.form['Body']
    number = request.form['From']

    if requested == 'pantry':
        foods = []
        for food in db.reference('items').get():
            foodData = db.reference('items/{0}'.format(food)).get()
            foods.append({
                'name': foodData['name'],
                'expiry': foodData['expiry']
                })
        sendMessage = ''
        for food in foods:
            sendMessage += food['name'] + ' ' + food['expiry'] + '\n'
        print(number)
        message = client.messages.create(
            to=number,
            from_="+12672146320",
            body=sendMessage)
    else:
        requested = requested.split(' ')
        entry = {
            'quantity': requested[0],
            'name': requested[1],
            'expiry': requested[2]
        }

        new_food = root.child('items').push(entry)

        # Start our response
        resp = MessagingResponse()

        # Add a message
        resp.message("Added! {0} ({1}) expires {2}".format(entry['name'], entry['quantity'], entry['expiry']))

        return str(resp)

# Load foods in website
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
        to="+16479815279",
        from_="+12672146320",
        body="anna ma"
        )
    warning = ''
    for food in foods:
        expdate = datetime.strptime(food['expiry'], '%Y-%m-%d').date()
        today = date.today()
        print(expdate, today, (expdate-today).days)
        if (expdate - today).days == 7:
            warning += '{0} expires in 7 days!'.format(food['name'])
    if warning != '':
        warningMessage = client.messages.create(
            to="+16479815279",
            from_="+12672146320",
            body=warning
            )
    print(message.sid)
    return render_template('index.html', foods = foods)

if __name__ == '__main__':
    app.run(debug=True)
