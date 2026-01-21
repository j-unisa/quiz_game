from flask import Flask, render_template, request
import sqlite3
from random import shuffle

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the homepage"""
    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()
    show_all = db.execute("SELECT * FROM q_a").fetchall()
    connection.close()
    return render_template("index.html", show_all=show_all)

@app.route('/quiz/<level>', methods=['GET', 'POST'])
def quiz(level):
    """
    Fetches questions for a specific difficulty level (easy/medium/hard),
    shuffles the answer options, and renders the quiz template.
    """
    # Security: whitelist allowed levels to prevent SQL injection or errors
    if level not in ['easy', 'medium', 'hard']:
        return render_template("index.html")

    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()

    query = "SELECT id, question, answer, option1, option2, option3 FROM q_a WHERE level = ? ORDER BY id"
    data = db.execute(query, (level,))
    
    # Convert tuples to lists so we can modify them (shuffle options)
    questions = list(map(list, data.fetchall()))
    connection.close()

    for row in questions:
        # Create a list of all options (Correct Answer + 3 Distractors)
        options = [row[2], row[3], row[4], row[5]]
        shuffle(options)

        # Overwrite the row with shuffled options so the correct answer isn't always first
        row[2] = options[0]
        row[3] = options[1]
        row[4] = options[2]
        row[5] = options[3]

    return render_template("quiz.html", questions=questions, level=level)

@app.route('/results', methods=["POST"])
def results():
    """
    Calculates the user's score by comparing form submissions against the database.
    """
    connection = sqlite3.connect('q_a.db')
    db = connection.cursor()

    level = request.form.get("level")

    # Fetch the correct answers for this level
    answers = db.execute("SELECT id, answer FROM q_a WHERE level=? ORDER BY id", (level,))
    answers = answers.fetchall()
    connection.close()

    score = 0
    correct_answers = {}
    for row in answers:
        correct_answers[row[0]] = row[1]

    # Loop through questions to check answers
    # Note: Relies on HTML inputs named 'question0', 'question1', etc.
    for row in range(len(correct_answers)):
        user_answer = request.form.get(f"question{row}")

        # Compare user answer vs correct answer
        if user_answer == list(correct_answers.values())[row]:
            score += 1

    # Prevent crash (division by zero) if a level has no questions
    if len(correct_answers) > 0:
        score_pct = int((score / len(correct_answers)) * 100)
    else:
        score_pct = 0

    return render_template("results.html", score=score_pct)

if __name__ == '__main__':
    app.run()
