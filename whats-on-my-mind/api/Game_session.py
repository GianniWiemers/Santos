from api import send_init_sets


class Game:
    def __init__(self, id_player_1, id_player_2, room):
        self.session_id = id_player_1[0:5] + id_player_2[0:5]
        self.room = room
        self.turn = id_player_1
        self.waiting = id_player_2
        ## id lists and image answers
        record_1, record_2, image_player1, image_player2 = create_image_set_session(conn)
        images_1 = None
        player_1_answer = None
        images_2 = None
        player_2_answer = None

        self.player_1 = Player(id=id_player_1, image_id_list=record_1, image_answer_id=image_player2)
        self.player_2 = Player(id=id_player_2, image_id_list=record_2, image_answer_id=image_player1)
        send_init_sets(room, images_1, images_2, player_1_answer, player_2_answer, self.turn, self.waiting)


    def handle_question(self, question_id, label, boolean_list):



class Player:

    def __init__(self, id, image_id_list, image_answer_id):
        self.id = id
        self.image_id_list = image_id_list
        self.selection_list = []
        self.prev_question_id = None
        self.label = None
        self.image_answer_id = image_answer_id

    def update_selection_list(self, selection_list):
        self.selection_list = selection_list

    def guess_image(self, guessed_image_id):
        return guessed_image_id == self.image_answer_id

    # def ask_question(self, question_id, label):
    #     for i in range(len(self.image_id_list)):
    #         if self.selection_list[i]:
    #             # insert labels
    #             insert_label(s)

    def update_question(self, question_id):
        self.prev_question_id = question_id

    def update_label(self, label):
        self.label = label
