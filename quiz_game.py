from flask import Flask, render_template, request
import sqlite3
from random import shuffle

app = Flask(__name__)

# Keeps track of amount of correct answers
score = {}


@app.route('/')
def index():

    # Creates access to database
    connection = sqlite3.connect('q_a.db')

    # Enables ability for SQL queries
    db = connection.cursor()

    show_all = db.execute("SELECT * FROM q_a")

    return render_template("index.html", show_all=show_all)


@app.route('/easy', methods=['GET', 'POST'])
def easy():

    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()

    # Fetches all easy questions
    easy = db.execute("SELECT id, question, answer, option1, option2, option3 FROM q_a WHERE level = 'easy'")

    # Turns tuples to lists. Turns map object to list
    easy_qs = list(map(list, easy.fetchall()))

    # Shuffle correct answer with all other answer options
    for row in easy_qs:
        options = [row[2], row[3], row[4], row[5]]
        shuffle(options)
        row[2] = options[0]
        row[3] = options[1]
        row[4] = options[2]
        row[5] = options[3]

    return render_template("easy.html", easy_qs=easy_qs)


@app.route('/medium')
def medium():

    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()

    # Fetches all medium questions
    medium = db.execute("SELECT id, question, answer, option1, option2, option3 FROM q_a WHERE level = 'medium'")

    # Turns tuples to lists. Turns map object to list
    medium_qs = list(map(list, medium.fetchall()))

    # Shuffle correct answer with all other answer options
    for row in medium_qs:
        options = [row[2], row[3], row[4], row[5]]
        shuffle(options)
        row[2] = options[0]
        row[3] = options[1]
        row[4] = options[2]
        row[5] = options[3]

    return render_template("medium.html", medium_qs=medium_qs)


@app.route('/hard')
def hard():

    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()

    # Fetches all hard questions
    hard = db.execute("SELECT id, question, answer, option1, option2, option3 FROM q_a WHERE level = 'hard'")

    # Turns tuples to lists. Turns map object to list
    hard_qs = list(map(list, hard.fetchall()))

    # Shuffle correct answer with all other answer options
    for row in hard_qs:
        options = [row[2], row[3], row[4], row[5]]
        shuffle(options)
        row[2] = options[0]
        row[3] = options[1]
        row[4] = options[2]
        row[5] = options[3]

    return render_template("hard.html", hard_qs=hard_qs)


@app.route('/results', methods=["POST"])
def results():

    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()

    # Retrieves all questions from specified level
    level = request.form.get("level")
    answers = db.execute("SELECT id, answer FROM q_a WHERE level=?", (level,))

    # List of tuples(one for each row)
    answers = answers.fetchall()

    # Dictionary of all correct answers
    correct_answers = {}
    for row in answers:
        correct_answers[row[0]] = row[1]

    # Initialize score
    score = 0

    for row in range(len(correct_answers)):
        answer = request.form.get(f"question{row}")

        # Compares user's answer to correct answer
        if answer == list(correct_answers.values())[row]:
            score += 1

    # User's amount of correct answers divided by amount of questions times 100 to get percentage
    score = int((score / len(correct_answers)) * 100)

    return render_template("results.html", score=score)


if __name__ == '__main__':
    app.run()
