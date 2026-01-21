# 🦄 The Super Smart Unicorn Quiz

A dynamic, database-driven quiz application built with Python and Flask. Designed to test knowledge across different difficulty levels with a fun, responsive user interface.

## 📋 Features

* **Dynamic Difficulty Levels:** Users can choose between **Easy**, **Medium**, and **Hard** modes.
* **Randomized Gameplay:**
    * Questions are fetched from a SQLite database.
    * Answer options (distractors) are shuffled every time so the correct answer position is never predictable.
* **Database Integration:** Content is stored in a structured SQL database (`q_a.db`), separating data from logic.
* **Instant Scoring:** Calculates percentage score immediately upon submission.
* **Responsive Design:** Custom CSS with a "Glassmorphism" card style, fully responsive for desktop and mobile.

## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, Jinja2 Templating
* **Architecture:** MVC (Model-View-Controller) pattern

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the repository
```bash
git clone https://github.com/j-unisa/quiz_game.git
cd quiz_game
```

### 2. Set up a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask
```

### 4. Database Setup

Ensure the `q_a.db` file is in the root directory. The database schema expects a table named `q_a` with the following columns:

* `id` (Integer)
* `level` (String: 'easy', 'medium', 'hard')
* `question` (String)
* `answer` (String)
* `option1`, `option2`, `option3` (Strings - Distractors)

### 5. Run the application
```bash
python quiz_game.py
```

The application will start at `http://127.0.0.1:5000/`.

## 📂 Project Structure
```bash
/unicorn-quiz
│
├── app.py                # Main Flask application logic (Routes & DB connections)
├── q_a.db                # SQLite database containing questions
├── static/
│   └── style.css         # Global styling (Typography, Colors, Layouts)
│   └── assets/           # Images and Fonts
├── templates/
│   ├── layout.html       # Base template (Header, Nav, Footer)
│   ├── index.html        # Homepage
│   ├── quiz.html         # Dynamic quiz form
│   └── results.html      # Score display page
└── README.md             # Project documentation
```

## 📝 License
This project is open source and available under the MIT License.

Coded with ❤️ in Henderson, NV.