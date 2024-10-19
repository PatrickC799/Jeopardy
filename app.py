import os
import random
import pandas as pd
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Path to your CSV file
CSV_FILE_PATH = '/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/Difficulty Classification/jeopardy_questions_with_difficulty.csv'  # Adjust to the actual path

# Load CSV data into a pandas DataFrame
def load_questions_from_csv():
    data = pd.read_csv(CSV_FILE_PATH)
    return data

# Function to get questions based on category and difficulty
def get_questions_for_category(data, category):
    category_data = data[data['Category'] == category]

    if category_data.empty:
        return None

    # Fetch 5 questions with difficulty levels from 1 to 5
    questions_by_difficulty = []
    for difficulty in range(1, 6):
        # Filter data for this specific difficulty
        difficulty_data = category_data[category_data['Difficulty'] == difficulty]

        # Check if there are questions for this difficulty
        if difficulty_data.empty:
            print(f"No questions found for {category} at difficulty {difficulty}")
            continue  # Skip if no questions are available for this difficulty

        # Sample a random question from the available ones
        question_row = difficulty_data.sample(n=1)
        question = {
            'question': question_row.iloc[0]['Questions'],
            'correct_answer': question_row.iloc[0]['Correct'],
            'answers': [
                question_row.iloc[0]['A'],
                question_row.iloc[0]['B'],
                question_row.iloc[0]['C'],
                question_row.iloc[0]['D']
            ],
            'difficulty': difficulty  # Keep track of the difficulty level
        }
        questions_by_difficulty.append(question)

    # If no questions were found for any difficulty, return None
    if not questions_by_difficulty:
        return None

    return questions_by_difficulty

# API endpoint to serve questions based on category
@app.route('/get_questions/<category>')
def get_questions(category):
    data = load_questions_from_csv()

    # Fetch questions from the specified category
    questions = get_questions_for_category(data, category)

    if not questions:
        return jsonify({'error': 'No questions found in this category'}), 404

    return jsonify(questions)

# Main game route
@app.route('/')
def index():
    data = load_questions_from_csv()

    # Get unique categories from the CSV file
    all_categories = data['Category'].unique().tolist()

    # Select only 3 random categories
    selected_categories = random.sample(all_categories, 3)

    return render_template('index.html', categories=selected_categories)

if __name__ == '__main__':
    app.run(debug=True)
