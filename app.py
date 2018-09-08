import firebase_admin, datetime
from firebase_admin import db, credentials
from flask import *
from tempfile import mkdtemp
# from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from datetime import timedelta, date, datetime
from operator import itemgetter

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
    requestedlist = requested.split(' ')
    number = request.form['From']

    if requested.lower() == 'pantry':
        # query database
        foods = []
        for food in db.reference('items').get():
            foodData = db.reference('items/{0}'.format(food)).get()

            # calculate days left until expiry
            expdate = datetime.strptime(foodData['expiry'], '%Y-%m-%d').date()
            today = date.today()
            daysleft = (expdate - today).days

            foods.append({
                'quantity': int(foodData['quantity']),
                'name': foodData['name'],
                'expiry': foodData['expiry'],
                'daysleft': daysleft
                })

        foods = sorted(foods, key = itemgetter('daysleft'))

        sendMessage = '\n\n' # initialize message

        for food in foods:
            if food['daysleft'] == 0:
                if food['quantity'] == 1:
                    sendMessage += u'\u2022' + ' ' + str(food['quantity']) + ' ' + food['name'] + ' expires TODAY!\n'
                else:
                    sendMessage += u'\u2022' + ' ' + str(food['quantity']) + ' ' + food['name'] + ' expire TODAY!\n'
            else:
                if food['quantity'] == 1 and food['daysleft'] == 1:
                    sendMessage += u'\u2022' + ' ' + str(food['quantity']) + ' ' + food['name'] + ' expires TOMMOROW!\n'
                elif food['quantity'] > 1 and food['daysleft'] == 1:
                    sendMessage += u'\u2022' + ' ' + str(food['quantity']) + ' ' + food['name'] + ' expire TOMMOROW!\n'
                elif food['quantity'] == 1 and food['daysleft'] > 1:
                    sendMessage += u'\u2022' + ' ' + str(food['quantity']) + ' ' + food['name'] + ' expires in ' + str(food['daysleft']) + ' days on ' + food['expiry'] + '\n'
                else:
                    sendMessage += u'\u2022' + ' ' + str(food['quantity']) + ' ' + food['name'] + ' expire in ' + str(food['daysleft']) + ' days on ' + food['expiry'] + '\n'
        message = client.messages.create(
            to=number,
            from_="+12672146320",
            body=sendMessage)
    elif requestedlist[0].lower() == 'add':
        requested = requested.split(' ')
        entry = {
            'quantity': requested[1],
            'name': ' '.join(requested[2:-1]).upper(),
            'expiry': requested[-1]
        }

        new_food = root.child('items').push(entry)

        # Start our response
        resp = MessagingResponse()

        # Add a message
        resp.message("Added! {0} ({1}) expires {2}".format(entry['name'], entry['quantity'], entry['expiry']))

        return str(resp)
    elif requestedlist[0].lower() == 'remove':
        requested = requested.split(' ')
        entry = {
            'quantity': requested[1],
            'name': ' '.join(requested[2:-1]).upper(),
            'expiry': requested[-1]
        }

        new_food = root.child('items').push(entry)

        # Start our response
        resp = MessagingResponse()

        # Add a message
        resp.message("Removed! {0} ({1}) expires {2}".format(entry['name'], entry['quantity'], entry['expiry']))

        return str(resp)

    return render_template('index.html')

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
