import time
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# this sets the flask session easily
# to access session variables import session from flask
SESSION_TYPE = 'sqlalchemy'
Session(app)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/findsession')
def find_session():
    pass

@app.route('/askquestion')
def ask_question():
    pass

@app.route('/sendresponse')
def send_question_response():
    pass

@app.route('/eliminate')
def update_image_tags():
    pass

@app.route('/guessimage')
def guess_image():
    pass
