import base64
import json
import time
from flask import Flask, request, Response, jsonify
from flask_session import Session
from flask_socketio import SocketIO, send, join_room, leave_room, emit
from flask_cors import CORS
from Game_session import Game
import database as db

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
app.config.from_object('config')

# this sets the flask session easily
# to access session variables import session from flask
SESSION_TYPE = 'sqlalchemy'
Session(app)

rooms_dict = {}  # {key=room_id, (Player1, Player2)}
players_dict = {}  # (key=Player, room_id)
games_dict = {}  # key=rooms, value=game
room_counter = 0
player_counter = 0

# get questions list
connection = db.create_connection("images.db")
question_list = db.get_questions(connection)
connection.close()

@socketio.on('connect')
def test_connect():
    print("Connected")


# player joins
# update player counter, room counter
# add player to room
# get player ids and create entry in rooms_dict
@socketio.on('initialize_player')
def initialize_player():
    print("joined")
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
        games_dict[room_counter] = Game(rooms_dict[room_counter][0], rooms_dict[room_counter][1], room_counter)
        room_counter += 1
    print("player_counter = " + str(player_counter))
    print("room_counter = " + str(room_counter))
    print("rooms_dict = " + str(rooms_dict))

    return Response("Done", 200)


def send_init_sets(room, images_1, images_2, player_1_answer, player_2_answer, player_turn_id, player_waiting_id):
    dict_player_1 = {'images_set': [base64.b64encode(x).decode("utf-8") for x in images_1],
                     'opponent_image': base64.b64encode(player_2_answer).decode("utf-8"),
                     'questions_list': [x[1] for x in question_list]}
    dict_player_2 = {'images_set': [base64.b64encode(x).decode("utf-8") for x in images_2],
                     'opponent_image': base64.b64encode(player_1_answer).decode("utf-8"),
                     'questions_list': [x[1] for x in question_list]}
    player_1 = rooms_dict[room][0]
    player_2 = rooms_dict[room][1]
    print(type(dict_player_1['images_set'][0]))
    emit("send_init_sets", json.dumps(dict_player_1, indent=4), to=player_1)
    emit("send_init_sets", json.dumps(dict_player_2, indent=4), to=player_2)
    emit("ask_question", to=player_turn_id)
    emit("wait", to=player_waiting_id)


# receive question and label
@socketio.on('send_question')
def receive_question(x):
    data = json.loads(x)
    room = players_dict[request.sid]
    game = games_dict[room]
    if game.handle_question(request.sid, question_list[int(data['question_id'])][0], data['label'], data['boolean_list']):
        question_json = {"question_id": data['question_id'], "label": data['label']}
        emit("wait", to=game.turn.id)
        emit("answer_question", json.dumps(question_json, indent=4), to=game.waiting.id) #check dumps


@socketio.on('send_answer')
def receive_answer(x):
    data = json.loads(x)
    room = players_dict[request.sid]
    game = games_dict[room]
    print(data)
    if game.handle_answer(request.sid, data['answer']):
        emit("ask_question", to=game.turn.id)
        emit("select_images", json.dumps(data['answer']), to=game.waiting.id)


@socketio.on('send_guess')
def receive_guess(x):
    data = json.loads(x)
    room = players_dict[request.sid]
    game = games_dict[room]
    if game.handle_guess(request.sid, data['guess']):
        emit("win", to=game.turn.id)
        emit("lose", to=game.waiting.id)
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
