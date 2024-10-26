import sqlite3

# Connect to the database
conn = sqlite3.connect('/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/Questions/jeopardy_data.db')

# Step 1: Create a new table with only the necessary columns
conn.execute('''
CREATE TABLE IF NOT EXISTS jeopardy_questions_cleaned (
    category TEXT,
    clue_value INTEGER,
    question TEXT,
    answer TEXT
)
''')

# Step 2: Copy the relevant data from the original table to the new table
conn.execute('''
INSERT INTO jeopardy_questions_cleaned (category, clue_value, question, answer)
SELECT category, clue_value, question, answer FROM jeopardy_questions
''')

# Step 3: Drop the old table
conn.execute("DROP TABLE jeopardy_questions")

# Step 4: Rename the cleaned table to the original table name
conn.execute("ALTER TABLE jeopardy_questions_cleaned RENAME TO jeopardy_questions")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Redundant columns removed and database optimized.")
