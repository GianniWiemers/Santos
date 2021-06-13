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
        api.send_init_sets(room, images_1, images_2, player_2_answer, player_1_answer, self.turn.id, self.waiting.id)

    # Handle a question, method is called whenever a question is sent trough the api
    def handle_question(self, requester, new_question_id, label, boolean_list):
        prev_selection_list = self.turn.selection_list
        if requester == self.turn.id:
            self.turn.update_selection_list(boolean_list)
            if self.turn.prev_answer == 2 or self.turn.prev_answer == 3:
                for i in range(len(self.turn.image_list)):
                    if self.turn.selection_list[i] and self.turn.prev_question_id is not None and \
                            self.turn.prev_label.strip() != '':
                        # Write annotation to db
                        db.create_annotation(connection, (self.session_id, self.turn.image_list[i][0],
                                                          self.turn.prev_question_id, self.turn.prev_label))
            if self.turn.prev_answer == 0 or self.turn.prev_answer == 1:
                for i in range(len(self.turn.image_list)):
                    if self.turn.selection_list[i] == False and prev_selection_list[i] == True and \
                            self.turn.prev_question_id is not None and self.turn.prev_label.strip() != '':
                        # Write annotation to db
                        db.create_annotation(connection, (self.session_id, self.turn.image_list[i][0],
                                                          self.turn.prev_question_id, self.turn.prev_label))
            self.turn.prev_question_id = new_question_id
            self.turn.prev_label = label
            return True
        else:
            return False

    # Handle answer
    def handle_answer(self, requester, answer):
        if requester == self.waiting.id:
            self.turn.prev_answer = answer
            self.switch_turns()
            return True
        return False

    def switch_turns(self):
        player_x = self.waiting
        self.waiting = self.turn
        self.turn = player_x

    def handle_guess(self, requester, guess, boolean_list):
        if requester == self.turn.id:
            prev_selection_list = self.turn.selection_list
            self.turn.update_selection_list(boolean_list)
            if self.turn.prev_answer == 2 or self.turn.prev_answer == 3:
                for i in range(len(self.turn.image_list)):
                    if self.turn.selection_list[i] and self.turn.prev_question_id is not None and \
                            self.turn.prev_label.strip() != '':
                        # Write annotation to db
                        db.create_annotation(connection, (self.session_id, self.turn.image_list[i][0],
                                                          self.turn.prev_question_id, self.turn.prev_label))
            if self.turn.prev_answer == 0 or self.turn.prev_answer == 1:
                for i in range(len(self.turn.image_list)):
                    if self.turn.selection_list[i] == False and prev_selection_list[i] == True and \
                            self.turn.prev_question_id is not None and self.turn.prev_label.strip() != '':
                        # Write annotation to db
                        db.create_annotation(connection, (self.session_id, self.turn.image_list[i][0],
                                                          self.turn.prev_question_id, self.turn.prev_label))
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
