from api import send_init_sets
import database as db
connection = db.create_connection()


# Class used for every game instance
class Game:
    def __init__(self, id_player_1, id_player_2, room):
        self.session_id = hash(id_player_1 + id_player_2)
        self.room = room
        ## id lists and image answers
        (record_1, record_2, image_player1, image_player2) = db.create_image_set_session(connection)
        images_1 = [x[1] for x in record_1]
        player_1_answer = image_player1[1]
        images_2 = [x[1] for x in record_2]
        player_2_answer = image_player2[1]

        self.player_1 = Player(id=id_player_1, image_id_list=record_1, image_answer_id=image_player2)
        self.player_2 = Player(id=id_player_2, image_id_list=record_2, image_answer_id=image_player1)
        self.turn = self.player_1
        self.waiting = self.player_2
        send_init_sets(room, images_1, images_2, player_1_answer, player_2_answer, self.turn, self.waiting)

    # Handle a question, method is called whenever a question is sent trough the api
    def handle_question(self, requester, new_question_id, label, boolean_list, connection):
        if requester == self.turn.id:
            self.turn.update_selection_list(boolean_list)
            if not self.turn.selection_list:
                for i in range(len(requester.image_id_list)):
                    if requester.selection_list[i]:
                        # send self.session_id + requester.label + image_id_list[i] + requester.prev_question_id to database
                        db.create_annotation(connection, (self.session_id, requester.image_id_list[i][0], requester.prev_question_id, requester.prev_label))
            self.waiting.prev_question_id = new_question_id
            self.waiting.prev_label = label
            return True
        else:
            return False

    # Handle answer
    def handle_answer(self, requester, answer):
        if requester == self.waiting:
            self.turn.prev_answer = answer
            self.switch_turns()
            return True
        return False

    def switch_turns(self):
        player_x = self.waiting
        self.waiting = self.turn
        self.turn = player_x

    def handle_guess(self, requester, guess):
        if requester == self.turn:
            if self.turn.guess_image(guess):
                return True
            else:
                self.switch_turns()
                return False

# Class that represents a player
class Player:

    def __init__(self, id, image_id_list, image_answer_id):
        self.id = id
        self.image_id_list = image_id_list
        self.selection_list = []
        self.prev_question_id = None
        self.prev_label = None
        self.prev_answer = None
        self.image_answer_id = image_answer_id

    def update_selection_list(self, selection_list):
        self.selection_list = selection_list

    def guess_image(self, guess):
        return self.image_id_list[guess][0] == self.image_answer_id[0]

    def update_question(self, question_id):
        self.prev_question_id = question_id

    def update_label(self, label):
        self.label = label
