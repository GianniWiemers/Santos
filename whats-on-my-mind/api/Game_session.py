import api
import database as db

connection = db.create_connection("images.db")


# Class used for every game instance
class Game:
    def __init__(self, id_player_1, id_player_2, room):
        ## Create session id
        self.session_id = hash(id_player_1 + id_player_2)
        self.room = room

        ## Image lists and answers
        (record_1, record_2, image_player1, image_player2) = db.create_image_set_session(connection)
        self.player_1 = Player(player_id=id_player_1, image_list=record_1, image_answer=image_player2)
        self.player_2 = Player(player_id=id_player_2, image_list=record_2, image_answer=image_player1)
        self.turn = self.player_1
        self.waiting = self.player_2

        ## Create lists with only images
        images_1 = [x[1] for x in record_1]
        player_1_answer = image_player1[1]
        images_2 = [x[1] for x in record_2]
        player_2_answer = image_player2[1]
        api.send_init_sets(room, images_1, images_2, player_1_answer, player_2_answer, self.turn.id, self.waiting.id)

    # Handle a question, method is called whenever a question is sent trough the api
    def handle_question(self, requester, new_question_id, label, boolean_list):
        if requester == self.turn.id:
            self.turn.update_selection_list(boolean_list)
            if not self.turn.selection_list:
                for i in range(len(requester.image_id_list)):
                    if requester.selection_list[i]:
                        # Write annotation to db
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

    def __init__(self, player_id, image_list, image_answer):
        self.id = player_id
        self.image_list = image_list
        self.selection_list = []
        self.prev_question_id = None
        self.prev_label = None
        self.prev_answer = None
        self.image_answer = image_answer

    def update_selection_list(self, selection_list):
        self.selection_list = selection_list

    def guess_image(self, guess):
        return self.image_list[guess][0] == self.image_answer[0]

    def update_question(self, question_id):
        self.prev_question_id = question_id

    def update_label(self, label):
        self.prev_label = label
