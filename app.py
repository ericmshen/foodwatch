import firebase_admin
from firebase_admin import db, credentials
from flask import *
from tempfile import mkdtemp

app = Flask(__name__)

app.secret_key = 'ericbmi500'

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

cred = credentials.Certificate('foodlord-5dd61-firebase-adminsdk-2ksfc-9d4371b135.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://foodlord-5dd61.firebaseio.com/'
    })

root = db.reference()

@app.route('/')
def index():
    new_food = root.child('items').push({
        'name': 'Banana',
        'expiry': '09/10/2018'
        })
    banana = db.reference('items/{0}'.format(new_food.key)).get()
    return render_template('index.html', banana = banana)

if __name__ == '__main__':
    app.run(debug=True)
