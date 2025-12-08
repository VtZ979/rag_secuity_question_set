import json
import re
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import nltk
import warnings

# Initialization runs only once
# Try to download stopwords, but if network fails, use cached data or default list
try:
    # Check if stopwords are already available
    try:
        stopwords.words('english')
        # If we can access it, it's already downloaded
    except LookupError:
        # Try to download silently
        nltk.download('stopwords', quiet=True)
except Exception as e:
    # If download fails, use a basic English stopwords list
    print(f"[WARNING] Could not download NLTK stopwords: {e}")
    print("[INFO] Using default English stopwords list")
    # Basic English stopwords as fallback
    stop_words = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
        'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
        'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
        'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
        'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
        'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
        'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
        'further', 'then', 'once'
    }
else:
    # Successfully loaded stopwords
    stop_words = set(stopwords.words('english'))

stemmer = PorterStemmer()

# Model and dictionary paths
MODEL_PATH = 'data/LDA_doc/lda_model_best_7topics.model'
DICT_PATH = 'data/LDA_doc/lda_dictionary.dict'
MAPPING_PATH = 'data/LDA_doc/topic_category_mapping.json'

# Load the model and dictionary
loaded_model = models.LdaModel.load(MODEL_PATH)
loaded_dict = corpora.Dictionary.load(DICT_PATH)

# Load the subject-class map
try:
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        topic_mapping = json.load(f)
except:
    topic_mapping = {}


# Text preprocessing functions
def preprocess_text(text):
    text = str(text)
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r'<code>.*?</code>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.lower().split()
    words = [stemmer.stem(w) for w in words if w not in stop_words and 2 <= len(w) <= 12]
    return ' '.join(words)


# Classification principal function
def classify_question(question):
    tokens = preprocess_text(question).split()
    bow = loaded_dict.doc2bow(tokens)
    topic_dist = loaded_model.get_document_topics(bow)

    if not topic_dist:
        return {
            "topic_id": None,
            "subcategory": "Unknown",
            "category": "Unknown",
            "distribution": []
        }

    best_topic = max(topic_dist, key=lambda x: x[1])[0]

    topic_info = topic_mapping.get(str(best_topic), {"subcategory": "Unknown", "category": "Unknown"})
    sub_cat = topic_info["subcategory"]
    main_cat = topic_info["category"]

    return {
        "topic_id": best_topic,
        "subcategory": sub_cat,
        "category": main_cat,
        "distribution": topic_dist
    }
