from flask import Flask, jsonify, render_template, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "secret_key_for_session_management"

# Define the difficulty ranges for clue_value
difficulty_ranges = {
    1: (0, 200),
    2: (300, 400),
    3: (500, 600),
    4: (700, 800),
    5: (900, 1000)
}

# Helper function to connect to the SQLite database
def get_db_connection():
    return sqlite3.connect('/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/Questions/jeopardy_data.db')

@app.route('/')
def index():
    # Connect to the database and select 3 random categories
    conn = get_db_connection()
    categories = conn.execute("SELECT DISTINCT category FROM jeopardy_questions ORDER BY RANDOM() LIMIT 3;").fetchall()
    conn.close()

    # Convert to list of category names
    category_list = [category[0] for category in categories]
    return render_template('index.html', categories=category_list)

def get_closest_question(category, min_value, max_value):
    conn = get_db_connection()
    query = """
    SELECT rowid, question, answer FROM jeopardy_questions
    WHERE category = ?
    AND clue_value BETWEEN ? AND ?
    ORDER BY RANDOM()
    LIMIT 1;
    """

    # Attempt to retrieve a question within the specified range
    result = conn.execute(query, (category, min_value, max_value)).fetchone()
    conn.close()

    # Expand range until a question is found
    while result is None and min_value > 0:
        min_value -= 200 if min_value > 0 else 0
        max_value += 200
        conn = get_db_connection()
        result = conn.execute(query, (category, min_value, max_value)).fetchone()
        conn.close()

    # If a question is found, check that it hasn't already been asked
    if result:
        question_id, question, answer = result
        asked_questions = set(session.get("asked_questions", []))

        if question_id not in asked_questions:
            asked_questions.add(question_id)
            session["asked_questions"] = list(asked_questions)
            return {"question": question, "correct_answer": answer}

    return None

@app.route('/get_questions/<category>/<int:difficulty>')
def get_questions(category, difficulty):
    if "asked_questions" not in session:
        session["asked_questions"] = []

    min_value, max_value = difficulty_ranges.get(difficulty, (0, 200))
    question_data = get_closest_question(category, min_value, max_value)
    print(f"Question data for category {category} and difficulty {difficulty}: {question_data}")

    return jsonify([question_data] if question_data else [])

if __name__ == '__main__':
    app.run(debug=True)
