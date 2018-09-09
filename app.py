import firebase_admin, datetime, re
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

def checkInt(i):
    try:
        int(i)
        return True
    except ValueError:
        return False

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    """Respond to incoming messages with a friendly SMS."""

    # Retrieve food data, store in list of dictionaries
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

    # Retrieve SMS information
    requested = request.form['Body']
    requestedlist = requested.split(' ')
    number = request.form['From']

    if requested.lower() == 'pantry':
        sendMessage = '\n\n' # initialize message

        # Print appropriate message for every food
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

        # Send message
        message = client.messages.create(
            to=number,
            from_="+12672146320",
            body=sendMessage)

    elif requestedlist[0].lower() == 'add':
        if not type(requestedlist[1]) != 'int' or re.search(r'^(\d{4})-(\d{2})-(\d{2})$', requestedlist[-1]) == None:
            # Start our response
            resp = MessagingResponse()

            # Add a message
            resp.message("Invalid format. Proper: add [quantity] [food] [yyyy-mm-dd]")

            return str(resp)
        elif int(requestedlist[1]) <= 0:
            # Start our response
            resp = MessagingResponse()

            # Add a message
            resp.message("Quantity must be greater than 0.")

            return str(resp)
        else:
            exists = False # Boolean for whether the thing is found
            entry = {
                'quantity': int(requestedlist[1]),
                'name': ' '.join(requestedlist[2:-1]).upper(),
                'expiry': requestedlist[-1]
            }

            for food in db.reference('items').get():
                foodData = db.reference('items/{0}'.format(food)).get()
                if entry['name'] == foodData['name'] and entry['expiry'] == foodData['expiry']:
                    foodKey = food
                    print(foodKey)
                    foodQuantity = foodData['quantity']
                    exists = True

            if exists == True:
                new_food = db.reference('items/{0}'.format(foodKey)).update({
                    'quantity': foodQuantity + entry['quantity']
                    })
            else:
                new_food = root.child('items').push(entry)

            # Start our response
            resp = MessagingResponse()

            # Add a message
            resp.message("Added! {0} ({1}) expires {2}".format(entry['name'], entry['quantity'], entry['expiry']))

            return str(resp)

    elif requestedlist[0].lower() == 'remove':
        if not checkInt(requestedlist[1]) and requestedlist[1] != 'all':
            # Start our response
            resp = MessagingResponse()

            # Add a message
            resp.message("Quantity must be greater than 0 or 'all'.")

            return str(resp)
        elif ' '.join(requestedlist[2:-1]).upper() not in [food['name'] for food in foods]:

            # Start our response
            resp = MessagingResponse()

            # Add a message
            resp.message("Food does not exist in pantry.")

            return str(resp)

        # Retrieve number of food in pantry
        for food in foods:
            if food['name'] == ' '.join(requestedlist[2:-1]).upper() and food['quantity'] == requestedlist[-1]:
                currentQ = food['quantity']

        entry = {
            'quantity': requestedlist[1],
            'name': ' '.join(requestedlist[2:-1]).upper(),
            'expiry': requestedlist[-1]
        }

        if requestedlist[1] == 'all':
            for food in db.reference('items').get():
                foodData = db.reference('items/{0}'.format(food)).get()
                if entry['name'] == foodData['name'] and entry['expiry'] == foodData['expiry']:
                    delete_food = db.reference('items/{0}'.format(food)).delete()

            # Start our response
            resp = MessagingResponse()

            # Add a message
            resp.message("Removed! {0} ({1}) expires {2}".format(entry['name'], entry['quantity'], entry['expiry']))

            return str(resp)

        elif int(requestedlist[1]) == currentQ:
            for food in db.reference('items').get():
                foodData = db.reference('items/{0}'.format(food)).get()
                if entry['name'] == foodData['name'] and entry['expiry'] == foodData['expiry']:
                    delete_food = db.reference('items/{0}'.format(food)).delete()

            # Start our response
            resp = MessagingResponse()

            # Add a message
            resp.message("Removed! {0} ({1}) expires {2}".format(entry['name'], entry['quantity'], entry['expiry']))

            return str(resp)

        elif int(requestedlist[1]) < currentQ:
            for food in db.reference('items').get():
                foodData = db.reference('items/{0}'.format(food)).get()
                if entry['name'] == foodData['name'] and entry['expiry'] == foodData['expiry']:
                    edit_food = db.reference('items/{0}'.format(food)).update({
                        'quantity': foodData['quantity'] - entry['quantity']
                        })

            # Start our response
            resp = MessagingResponse()

            # Add a message
            resp.message("Removed! {0} ({1}) expires {2}".format(entry['name'], entry['quantity'], entry['expiry']))

            return str(resp)

        else:
            # Start our response
            resp = MessagingResponse()

            # Add a message
            resp.message("Invalid input.")

            return str(resp)

    else:
        # Start our response
        resp = MessagingResponse()

        # Add a message
        resp.message("Invalid command.")

        return str(resp)

    return render_template('index.html')

# Load foods in website
@app.route('/')
def index():
    foods = []
    for food in db.reference('items').get():
        foodData = db.reference('items/{0}'.format(food)).get()

        # calculate days left until expiry
        expdate = datetime.strptime(foodData['expiry'], '%Y-%m-%d').date()
        today = date.today()
        daysleft = (expdate - today).days

        foods.append({
            'name': foodData['name'],
            'quantity': str(foodData['quantity']),
            'expiry': foodData['expiry'],
            'daysleft': daysleft
            })

    # test message
    message = client.messages.create(
        to="+16479815279",
        from_="+12672146320",
        body="stravinsky = GOAT"
        )

    warning = ''
    for food in foods:
        expdate = datetime.strptime(food['expiry'], '%Y-%m-%d').date()
        today = date.today()
        print(expdate, today, (expdate-today).days)
        if (expdate - today).days == 0:
            warning += u'\u2022' + ' ' + '{0} expires TODAY!'.format(food['name']) + '\n'
        elif (expdate - today).days == 1:
            warning += u'\u2022' + ' ' + '{0} expires TOMORROW!'.format(food['name']) + '\n'
        elif (expdate - today).days == 3:
            warning += u'\u2022' + ' ' + '{0} expires in 3 days!'.format(food['name']) + '\n'
        elif (expdate - today).days == 7:
            warning += u'\u2022' + ' ' + '{0} expires in 7 days!'.format(food['name']) + '\n'

    if warning != '':
        warningMessage = client.messages.create(
            to="+16479815279",
            from_="+12672146320",
            body=warning
            )

    print(message.sid)

    foods = sorted(foods, key = itemgetter('expiry'))

    return render_template('index.html', foods = foods)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/remove')
def remove():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
