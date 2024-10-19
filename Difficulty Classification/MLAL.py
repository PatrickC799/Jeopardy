import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Load the CSV data
df = pd.read_csv('/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/CSV/consolidated_trivia.csv')

# Create a new column for difficulty labels (initially NaN)
df['Difficulty'] = np.nan

# Randomly sample questions for manual labeling
sample_size = 10  # Adjust the number of questions to label manually each iteration
sample_questions = df[df['Difficulty'].isna()].sample(sample_size, random_state=42)

print("Please label the following questions with difficulty (1-5):")

# Loop through each sampled question and collect manual input
for idx, row in sample_questions.iterrows():
    print(f"\nQuestion: {row['Questions']}")
    while True:
        try:
            difficulty = int(input("Enter difficulty level (1: Easy, 5: Hard): "))
            if difficulty in [1, 2, 3, 4, 5]:
                df.loc[idx, 'Difficulty'] = difficulty  # Use loc[] to avoid the warning
                break
            else:
                print("Please enter a valid difficulty (1-5).")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

# Split data into labeled and unlabeled sets
labeled_df = df[df['Difficulty'].notna()]
unlabeled_df = df[df['Difficulty'].isna()]

# Vectorize the questions using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')

# Use labeled data to train a classifier
X_labeled = vectorizer.fit_transform(labeled_df['Questions'])
y_labeled = labeled_df['Difficulty']

# Train a RandomForestClassifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_labeled, y_labeled)

# Predict difficulties for the unlabeled data
X_unlabeled = vectorizer.transform(unlabeled_df['Questions'])
predicted_difficulties = clf.predict(X_unlabeled)

# Assign predicted difficulties to the unlabeled data using loc[] to avoid the warning
df.loc[unlabeled_df.index, 'Difficulty'] = predicted_difficulties

# --- Active learning step: ---
# Get prediction probabilities
probabilities = clf.predict_proba(X_unlabeled)
confidence_scores = probabilities.max(axis=1)

# Sort unlabeled questions by lowest confidence
most_uncertain_indices = np.argsort(confidence_scores)[:sample_size]
uncertain_questions = unlabeled_df.iloc[most_uncertain_indices]

print("\nMost uncertain questions for further manual labeling:")
# Use predicted difficulties directly from the `predicted_difficulties` array
for i, (idx, row) in enumerate(uncertain_questions.iterrows()):
    print(f"\nQuestion: {row['Questions']} | Predicted Difficulty: {predicted_difficulties[most_uncertain_indices[i]]}")
    while True:
        try:
            difficulty = int(input("Enter difficulty level (1: Easy, 5: Hard): "))
            if difficulty in [1, 2, 3, 4, 5]:
                df.loc[idx, 'Difficulty'] = difficulty  # Use loc[] to update the main dataframe
                break
            else:
                print("Please enter a valid difficulty (1-5).")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

# Save the results
df.to_csv('jeopardy_questions_with_active_learning.csv', index=False)

print("Active learning complete. Output saved to 'jeopardy_questions_with_active_learning.csv'")
