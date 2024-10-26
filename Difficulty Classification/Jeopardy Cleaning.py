import pandas as pd
import glob
import os

# Define file path pattern
folder_path = '/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/Difficulty Classification/jeopardy_clue_dataset/seasons'
file_pattern = os.path.join(folder_path, 'season*.tsv')

# Define the difficulty ranges
difficulty_ranges = {
    1: (0, 200),
    2: (300, 400),
    3: (500, 600),
    4: (700, 800),
    5: (900, 1000)
}

# Function to check if a category has at least one question in each range
def has_full_difficulty_coverage(category_data):
    for min_value, max_value in difficulty_ranges.values():
        if category_data[(category_data['clue_value'] >= min_value) & (category_data['clue_value'] <= max_value)].empty:
            return False
    return True

# List to store all filtered data
filtered_data = []

# Process each file
for file_path in glob.glob(file_pattern):
    # Load the TSV file
    season_data = pd.read_csv(file_path, sep='\t')
    season_data['clue_value'] = pd.to_numeric(season_data['clue_value'], errors='coerce').fillna(0).astype(int)

    # Filter out categories without full difficulty coverage
    qualified_season_data = season_data.groupby('category').filter(has_full_difficulty_coverage)

    # Append the filtered data to the list
    filtered_data.append(qualified_season_data)

# Concatenate all the filtered data
combined_data = pd.concat(filtered_data, ignore_index=True)

# Save the cleaned dataset to a single TSV file
output_file = '/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/Difficulty Classification/cleaned_combined_jeopardy_data.tsv'
combined_data.to_csv(output_file, sep='\t', index=False)

print(f"Cleaned and combined dataset saved to {output_file} with {len(combined_data['category'].unique())} qualifying categories.")
