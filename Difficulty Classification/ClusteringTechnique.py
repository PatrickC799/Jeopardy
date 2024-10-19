import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load the CSV data
# Adjust the file path if needed
df = pd.read_csv('/Users/patrickcunningham/LeetCode/Jeapordy/pythonProject/CSV/consolidated_trivia.csv')

# Vectorize the questions using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['Questions'])

# Perform KMeans clustering, assuming 5 levels of difficulty
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['DifficultyCluster'] = kmeans.fit_predict(X)

# Map cluster numbers to difficulty levels (1-5)
df['Difficulty'] = df['DifficultyCluster'] + 1  # Assuming cluster 0 is the easiest

# Save the resulting dataframe with difficulty levels to a new CSV
df.to_csv('jeopardy_questions_with_difficulty.csv', index=False)

print("Clustering complete. Output saved to 'jeopardy_questions_with_difficulty.csv'")

