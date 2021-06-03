import database as db

if __name__ == '__main__':
    # Uncomment this to create the database
    # db.create("images.db")

    conn = db.create_connection("images.db")

    questions = ["Does the image contain $?", "Is the image related to $?"]

    # db.create_question(conn, ("Does the image contain $?",))
    # db.create_question(conn, ("Is the image related to $?",))
    # daggoes, paard, olifant, vlinder, haan, kat, koe, schaap, spin, eekhoorn = [], [], [], [], [], [], [], [], [], []
    # for i in range(1, 21):
    #    daggoes.append('raw-img/cane/' + str(i) + '.jpeg')
    #    paard.append('raw-img/cavallo/' + str(i) + '.jpeg')
    #    olifant.append('raw-img/elefante/' + str(i) + '.jpg')
    #    vlinder.append('raw-img/farfalla/' + str(i) + '.jpg')
    #    haan.append('raw-img/gallina/' + str(i) + '.jpeg')
    #    kat.append('raw-img/gatto/' + str(i) + '.jpeg')
    #    koe.append('raw-img/mucca/' + str(i) + '.jpeg')
    #    schaap.append('raw-img/pecora/' + str(i) + '.jpg')
    #    spin.append('raw-img/ragno/' + str(i) + '.jpg')
    #    eekhoorn.append('raw-img/scoiattolo/' + str(i) + '.jpeg')

    # animals = [daggoes, paard, olifant, vlinder, haan, kat, koe, schaap, spin, eekhoorn]

    with conn:
        # for animal in animals:
        #    # Create image
        #    for i in range(0, 20):
        #        blob_image = db.convertToBinaryData(animal[i])
        #        image_id = db.create_image(conn, (blob_image,))

        # Gets 40 images, image set for player 1, player 2 and the image of player 1, player 2,
        set_p1, set_p2, player1, player2 = db.create_image_set_session(conn)

        questions = db.get_questions(conn)

        print(questions)

        # Writes images of players to disk:
        # db.write_blob(str(player1[0]), player1[1])
        # db.write_blob(str(player2[0]), player2[1])
