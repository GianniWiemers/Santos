from flask import Flask, render_template
from flask_socketio import SocketIO, send, join_room
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def hello_world():
    return 'Hello World!'

@socketio.on('message')
def handle_message(data):
    print(data)
    send(data, broadcast=True)

@socketio.on('join')
def on_join(data):
    join_room(data)
    send("somebody has entered room " + data, to=data)


if __name__ == '__main__':
    socketio.run(app)