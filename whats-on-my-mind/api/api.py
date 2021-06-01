import json
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
@socketio.on('send_question')
def receive_question():
    room = players_dict[request.sid]
    data = request.json
    game = games_dict[room]
    if game.handle_question(request.sid, data['question_id'], data['label'], data['boolean_list']):
        question_json = {"question_id": data['question_id'], "label": data['label']}
        emit("wait", to=game.turn)
        emit("answer_question", json.dumps(question_json, indent=4), to=game.waiting)

@socketio.on('send_answer')
def receive_answer():
    room = players_dict[request.sid]
    data = request.json
    game = games_dict[room]
    if game.handle_answer(request.sid, data['answer']):
        emit("ask_question", to=game.turn.id)
        emit("wait", to=game.waiting.id)

@socketio.on('send_guess')
def receive_guess():
    room = players_dict[request.sid]
    data = request.json
    game = games_dict[room]
    if game.handle_guess(request.sid, data['guess']):
        emit("win", to=game.turn)
        emit("lose", to=game.waiting)
    else:
        emit("ask_question", to=game.turn.id)
        emit("wait", to=game.waiting.id)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')

# @socketio.on('leave')
# def on_leave(data):
#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send(username + ' has left the room.', to=room)
