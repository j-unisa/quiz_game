# Quiz game will store several questions and answers in a SQL database.

from flask import Flask, render_template, request
import sqlite3
from random import choice

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
    easy = db.execute("SELECT question, answer, option1, option2, option3 FROM q_a WHERE level = 'easy'")

    # List of tuples(one tuple for each row)
    easy_qs = easy.fetchall()

    """
    # Creates list of easy question id's
    easy_qs_nums = [row[0] for row in easy_qs_nums]

    # Random id is chosen
    question_num = choice(easy_qs_nums)

    # Removes id from list
    easy_qs_nums.remove(question_num)

    table = db.execute("SELECT question, answer, option1, option2, option3"
                       " FROM q_a WHERE id = ?", (question_num,))

    question = row[0]
    answer = row[1]
    option1 = row[2]
    option2 = row[3]
    option3 = row[4]
    """

    question1 = request.form.get("question1")
    question2 = request.form.get("question2")
    question3 = request.form.get("question3")
    question4 = request.form.get("question4")

    return render_template("easy.html", easy_qs=easy_qs)


@app.route('/medium')
def medium():

    return render_template("medium.html")


@app.route('/hard')
def hard():

    return render_template("hard.html")


if __name__ == '__main__':
    app.run()
