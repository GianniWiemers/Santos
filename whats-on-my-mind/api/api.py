import time
from flask import Flask, request, Response
from flask_session import Session
from flask_socketio import SocketIO, send, join_room, leave_room
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
app.config.from_object('config')

db = SQLAlchemy(app)

# this sets the flask session easily
# to access session variables import session from flask
SESSION_TYPE = 'sqlalchemy'
Session(app)

rooms_dict = {}  # {key=room_id, (Player1, Player2)}
players_dict = {} # (key=Player, room_id)
room_counter = 0
player_counter = 0



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


@socketio.on('message')
def handle_message(data):
    print(data)
    send(data, broadcast=True)


@socketio.on('join')
def on_join(data):
    print(request.sid)
    room = "1"
    join_room(room)
    send('Somebody has entered the room.', to=room)


# player joins
# update player counter, room counter
# add player to room
# get player ids and create entry in rooms_dict
@socketio.on('initialize_player')
def initialize_player():
    global player_counter
    global room_counter
    player_id = request.sid
    if player_counter == 0:
        player_counter = player_counter + 1
        join_room(str(room_counter))
        rooms_dict[room_counter] = [player_id]
        players_dict[player_id] = room_counter

    elif player_counter == 1:
        player_counter = 0
        join_room(str(room_counter))
        rooms_dict[room_counter].append(player_id)
        players_dict[player_id] = room_counter
        room_counter = room_counter + 1
    print("player_counter = " + str(player_counter))
    print("room_counter = " + str(room_counter))
    print("rooms_dict = " + str(rooms_dict))

    return Response("Done", 200)

@socketio.on('message_opponent')
def message_opponent(data):
    print(data)
    room_id = players_dict[request.sid]
    player_id_list = rooms_dict[room_id]
    opponent_id = ""
    for i in player_id_list:
        if i is not request.sid:
            opponent_id = i
    print(room_id)
    send("Hi fella", to=opponent_id)

@socketio.on('connect')
def test_connect():
    print("ass")

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')

# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', to=room)
