from flask import Flask, render_template, request
import sqlite3
from random import shuffle

app = Flask(__name__)

# Keeps track of amount of correct answers
score = {}

@app.route('/')
def index():
    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()
    # You generally don't need to fetch *all* data for the index unless you are displaying it there
    # But keeping your original logic for now:
    show_all = db.execute("SELECT * FROM q_a")
    return render_template("index.html", show_all=show_all)

# --- THIS IS THE NEW DYNAMIC ROUTE ---
@app.route('/quiz/<level>', methods=['GET', 'POST'])
def quiz(level):
    # 1. Security check: prevent users from typing /quiz/garbage
    if level not in ['easy', 'medium', 'hard']:
        return render_template("index.html")

    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()

    # 2. Use the 'level' variable to get the right questions
    # Note: We select specific columns to ensure index 2 is always the answer
    query = "SELECT id, question, answer, option1, option2, option3 FROM q_a WHERE level = ?"
    data = db.execute(query, (level,))
    
    questions = list(map(list, data.fetchall()))

    # 3. Shuffle logic (identical to before, but now works for all levels)
    for row in questions:
        options = [row[2], row[3], row[4], row[5]]
        shuffle(options)
        row[2] = options[0]
        row[3] = options[1]
        row[4] = options[2]
        row[5] = options[3]

    # 4. Render the SINGLE generic template
    return render_template("quiz.html", questions=questions, level=level)

@app.route('/results', methods=["POST"])
def results():
    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()

    level = request.form.get("level")
    answers = db.execute("SELECT id, answer FROM q_a WHERE level=?", (level,))
    answers = answers.fetchall()

    correct_answers = {}
    for row in answers:
        correct_answers[row[0]] = row[1]

    score = 0
    for row in range(len(correct_answers)):
        # We need to make sure we look for the right question ID in the form
        # Note: This loop relies on the form naming convention 'question0', 'question1', etc.
        answer = request.form.get(f"question{row}")
        if answer == list(correct_answers.values())[row]:
            score += 1

    # Avoid division by zero if database is empty
    if len(correct_answers) > 0:
        score_pct = int((score / len(correct_answers)) * 100)
    else:
        score_pct = 0

    return render_template("results.html", score=score_pct)

if __name__ == '__main__':
    app.run()
    