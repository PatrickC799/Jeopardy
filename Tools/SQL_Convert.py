import pandas as pd
import sqlite3

# Load the cleaned combined dataset
combined_data = pd.read_csv('/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/Difficulty Classification/cleaned_combined_jeopardy_data.tsv', sep='\t')

# Connect to SQLite database (creates a file called jeopardy_data.db if it doesn't exist)
conn = sqlite3.connect('/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/Questions/jeopardy_data.db')

# Write the DataFrame to SQLite
combined_data.to_sql('jeopardy_questions', conn, if_exists='replace', index=False)

# Create indexes for faster lookups on category and clue_value
with conn:
    conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON jeopardy_questions (category);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_clue_value ON jeopardy_questions (clue_value);")

# Close the connection
conn.close()
