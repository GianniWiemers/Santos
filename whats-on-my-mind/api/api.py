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
players_dict = {}  # (key=Player, room_id)
room_counter = 0
player_counter = 0


@socketio.on('connect')
def test_connect():
    print("Connected")


# player joins
# update player counter, room counter
# add player to room
# get player ids and create entry in rooms_dict
@socketio.on('initialize_player')
def initialize_player():
    global player_counter
    global room_counter
    player_id = request.sid
    join_room(str(room_counter))
    players_dict[player_id] = room_counter
    if player_counter == 0:
        player_counter += 1
        rooms_dict[room_counter] = [player_id]
    elif player_counter == 1:
        player_counter = 0
        rooms_dict[room_counter].append(player_id)
        room_counter += 1

    print("player_counter = " + str(player_counter))
    print("room_counter = " + str(room_counter))
    print("rooms_dict = " + str(rooms_dict))

    return Response("Done", 200)


# test messaging opponent
@socketio.on('message_opponent')
def message_opponent(data):
    print(data)
    room_id = players_dict[request.sid]
    player_id_list = rooms_dict[room_id]
    opponent_id = player_id_list[0]
    if player_id_list[1] != request.sid:
        opponent_id = player_id_list[0]
    print(room_id)
    send("Message to opponent in room: " + str(room_id), to=opponent_id)


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

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')

# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', to=room)
