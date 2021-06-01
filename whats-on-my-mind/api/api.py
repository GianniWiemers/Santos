import time
from flask import Flask, request, Response, jsonify
from flask_session import Session
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from Game_session import Game
from enum import Enum, auto

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
games_dict = {} # key=rooms, value=game
room_counter = 0
player_counter = 0

# get questions list
# question_list = get_database_question_list
question_list = None

dummy_images_1 = ["a", "b", "c", "d", "e", "f"]
dummy_guess_image_1 = "1"
dummy_images_2 = ["1", "2", "3", "4", "5", "6"]
dummy_guess_image_2 = "b"

ASK = "ASK"
WAIT_RESPONSE = "WAIT_RESPONSE"
WAIT_QUESTION = "WAIT_QUESTION"
RECEIVE_ANSWER = "RECEIVE_ANSWER"


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
        games_dict[room_counter] = Game(rooms_dict[0], [1], room_counter)
        room_counter += 1
    print("player_counter = " + str(player_counter))
    print("room_counter = " + str(room_counter))
    print("rooms_dict = " + str(rooms_dict))

    return Response("Done", 200)


def send_init_sets(room, images_1, images_2, player_1_answer, player_2_answer, player_turn_id, player_waiting_id):
    dict_player_1 = {'images_set': images_1, 'opponent_image': player_2_answer, 'questions_list': question_list}
    dict_player_2 = {'images_set': images_2, 'opponent_image': player_1_answer, 'questions_list': question_list}
    player_1 = rooms_dict[room][0]
    player_2 = rooms_dict[room][1]
    emit("send_init_sets", jsonify(dict_player_1), to=player_1)
    emit("send_init_sets", jsonify(dict_player_2), to=player_2)
    emit("ask_question", to=player_turn_id)
    emit("wait", to=player_waiting_id)

# receive question and label
@socketio.on('receive_question')
def receive_question():
    room = players_dict[request.sid]
    data = request.json
    game = games_dict[room]
    game.handle_question(data['question'], data['label'], data['boolean_list'])


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
