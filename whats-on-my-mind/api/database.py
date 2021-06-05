import sqlite3
import random


def create_connection(name_db):
    conn = None
    try:
        conn = sqlite3.connect(name_db)
    except sqlite3.Error as er:
        print(er)

    return conn


def create_table(conn, table_sql):
    try:
        c = conn.cursor()
        c.execute(table_sql)
    except sqlite3.Error as er:
        print(er)


def create_image(conn, image):
    sql = ''' INSERT INTO images(image) VALUES (?) '''

    cur = conn.cursor()
    cur.execute(sql, image)
    conn.commit()

    return cur.lastrowid


def create_annotation(conn, session):
    sql = ''' INSERT INTO sessions(session_id, image_id, question_id, label) VALUES (?, ?, ?, ?) '''

    cur = conn.cursor()
    cur.execute(sql, session)
    conn.commit()

    return cur.lastrowid


def create_question(conn, question):
    sql = ''' INSERT INTO questions(question) VALUES (?) '''

    cur = conn.cursor()
    cur.execute(sql, question)
    conn.commit()

    return cur.lastrowid


def convertToBinaryData(filename):
    with open(filename, 'rb') as f:
        blob = f.read()
    return blob


def create(database_name):
    create_images_table = """CREATE TABLE IF NOT EXISTS images (
                                id integer PRIMARY KEY, 
                                image BLOB NOT NUll
                            );"""

    create_questions_table = """CREATE TABLE IF NOT EXISTS questions (
                                id integer PRIMARY KEY, 
                                question text NOT NULL 
                            );"""

    create_sessions_table = """ CREATE TABLE IF NOT EXISTS sessions (
                                session_id integer NOT NULL,
                                image_id integer NOT NULL,
                                question_id integer NOT NULL,
                                label text NOT NULL,
                                PRIMARY KEY (session_id, image_id, question_id, label),
                                FOREIGN KEY (image_id) REFERENCES images (id),
                                FOREIGN KEY (question_id) REFERENCES questions (id)
                            );"""

    conn = create_connection(database_name)

    with conn:
        if conn is not None:
            create_table(conn, create_images_table)

            create_table(conn, create_questions_table)

            create_table(conn, create_sessions_table)
        else:
            print("Ewa sa7 ik kan niet connecten")


def create_image_set_session(conn):
    image_query = """SELECT * FROM images ORDER BY RANDOM() LIMIT 40"""
    cur = conn.cursor()
    cur.execute(image_query)

    # Contains 40 random images (no duplicates)
    record = cur.fetchall()

    cur.close()

    middle = len(record) // 2
    image_set_p1 = record[:middle]
    image_set_p2 = record[middle:]

    image_player1 = random.sample(image_set_p2, 1)[0]
    image_player2 = random.sample(image_set_p1, 1)[0]

    return image_set_p1, image_set_p2, image_player1, image_player2


def get_questions(conn):
    question_query = """SELECT * FROM questions"""
    cur = conn.cursor()
    cur.execute(question_query)

    # Contains all questions
    questions = cur.fetchall()

    cur.close()

    return questions


# Writes blob image to disk (for debugging?)
def write_blob(name, blob):
    with open(name + ".jpg", 'wb') as file:
        file.write(blob)
    print("Written blob to: ", name, "\n")
