import spacy
import nltk
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from textblob import TextBlob

nltk.download('punkt')
nltk.download('stopwords')

def extract_topics(text, num_topics=2):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words and t not in string.punctuation]

    # Adjusting TfidfVectorizer for short texts
    tfidf_vectorizer = TfidfVectorizer(max_df=1.0, min_df=1, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform([' '.join(tokens)])
    nmf = NMF(n_components=num_topics, random_state=1).fit(tfidf)

    feature_names = tfidf_vectorizer.get_feature_names_out()
    topics = [feature_names[i] for i in nmf.components_.argsort()[0, :-num_topics-1:-1]]
    return topics

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    return 'positive' if sentiment_polarity > 0 else 'negative' if sentiment_polarity < 0 else 'neutral'

def process_text(text):
    topics = extract_topics(text)
    sentiment = analyze_sentiment(text)
    return topics, sentiment