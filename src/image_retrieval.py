import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

nltk.download('punkt')
nltk.download('stopwords')

# Load the datasets
def load_data():
    photos = pd.read_csv('../data/photos.tsv', sep='\t')
    keywords = pd.read_csv('../data/keywords.tsv', sep='\t')
    merged_data = pd.merge(photos, keywords, on='photo_id')
    return merged_data

# Text processing and topic extraction
def extract_topics(text, num_topics=1):
    # Tokenize and clean text
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stopwords.words('english') and t not in string.punctuation]

    # Create a TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform([' '.join(tokens)])
    nmf = NMF(n_components=num_topics, random_state=1).fit(tfidf)

    # Extract the topic
    feature_names = tfidf_vectorizer.get_feature_names_out()
    topics = [feature_names[i] for i in nmf.components_.argsort()[0, :-num_topics-1:-1]]
    return topics

# Retrieve images based on topics and emotion
def retrieve_images(data, topics, emotion):
    # Convert topics and emotion to lowercase to match keywords
    search_terms = [term.lower() for term in topics] + [emotion.lower()]
    # Filter data for photos matching any of the search terms
    filtered_data = data[data['keyword'].str.lower().isin(search_terms)]
    # Select distinct photo URLs
    image_urls = filtered_data['photo_image_url'].drop_duplicates().tolist()
    return image_urls

def main(input_text, emotion):
    topics = extract_topics(input_text)
    topics.append(emotion)
    images = retrieve_images(data, topics)
    return images

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = ' '.join(sys.argv[1:])
        main(input_text)
    else:
        print("Usage: python image_retrieval.py 'input text here'")