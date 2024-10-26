import pandas as pd
from flask import Flask, jsonify, render_template, session
import random

app = Flask(__name__)
app.secret_key = "secret_key_for_session_management"

# Load the dataset
data = pd.read_csv('/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/Difficulty Classification/cleaned_jeopardy_data.tsv', sep='\t')
data['clue_value'] = pd.to_numeric(data['clue_value'], errors='coerce').fillna(0).astype(int)

# Mapping difficulty levels to `clue_value` ranges
difficulty_ranges = {
    1: (0, 200),
    2: (300, 400),
    3: (500, 600),
    4: (700, 800),
    5: (900, 1000)
}

@app.route('/')
def index():
    # Select categories for display
    categories = data['category'].drop_duplicates().sample(3).tolist()
    return render_template('index.html', categories=categories)

def get_closest_question(category, min_value, max_value):
    category_questions = data[data['category'] == category]
    filtered_data = category_questions[(category_questions['clue_value'] >= min_value) & (category_questions['clue_value'] <= max_value)]

    while filtered_data.empty:
        min_value -= 200 if min_value > 0 else 0
        max_value += 200
        filtered_data = category_questions[(category_questions['clue_value'] >= min_value) & (category_questions['clue_value'] <= max_value)]

    for _, row in filtered_data.iterrows():
        question_id = row.name
        asked_questions = set(session.get("asked_questions", []))
        if question_id not in asked_questions:
            asked_questions.add(question_id)
            session["asked_questions"] = list(asked_questions)
            return {
                "question": row['question'],
                "correct_answer": row['answer']
            }
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
