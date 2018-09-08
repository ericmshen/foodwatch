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

# root = db.reference()

@app.route('/')
def index():
    foods = []
    for food in db.reference('items').get():
        foodData = db.reference('items/{0}'.format(food)).get()
        foods.append({
            'name': foodData['name'],
            'expiry': foodData['expiry']
            })
    return render_template('index.html', foods = foods)

if __name__ == '__main__':
    app.run(debug=True)
