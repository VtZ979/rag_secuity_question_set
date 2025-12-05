"""
LDA Topic Classification for Security Questions
"""
import json
import re
from pathlib import Path
from gensim import corpora, models
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import nltk

# Download stopwords if not available
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


class LDAClassifier:
    """
    LDA-based topic classifier for security questions.
    """
    
    def __init__(self, model_path=None, dict_path=None, mapping_path=None):
        """
        Initialize the LDA classifier.
        
        Args:
            model_path: Path to LDA model file
            dict_path: Path to dictionary file
            mapping_path: Path to topic-category mapping JSON
        """
        self.model = None
        self.dictionary = None
        self.topic_mapping = {}
        
        if model_path and dict_path:
            self.load_model(model_path, dict_path, mapping_path)
    
    def load_model(self, model_path, dict_path, mapping_path=None):
        """
        Load LDA model and dictionary.
        
        Args:
            model_path: Path to LDA model
            dict_path: Path to dictionary
            mapping_path: Path to topic mapping JSON
        """
        self.model = models.LdaModel.load(str(model_path))
        self.dictionary = corpora.Dictionary.load(str(dict_path))
        
        if mapping_path and Path(mapping_path).exists():
            try:
                with open(mapping_path, "r", encoding="utf-8") as f:
                    self.topic_mapping = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load topic mapping: {e}")
                self.topic_mapping = {}
    
    def preprocess_text(self, text):
        """
        Preprocess text for LDA classification.
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Preprocessed text string
        """
        text = str(text)
        # Remove HTML tags
        text = BeautifulSoup(text, "html.parser").get_text()
        # Remove code blocks
        text = re.sub(r'<code>.*?</code>', '', text)
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize and stem
        words = text.lower().split()
        words = [
            stemmer.stem(w) 
            for w in words 
            if w not in stop_words and 2 <= len(w) <= 12
        ]
        return ' '.join(words)
    
    def classify(self, question):
        """
        Classify a question into a security topic.
        
        Args:
            question: Question text to classify
            
        Returns:
            Dictionary with topic_id, subcategory, category, and distribution
        """
        if self.model is None or self.dictionary is None:
            return {
                "topic_id": None,
                "subcategory": "Unknown",
                "category": "Unknown",
                "distribution": []
            }
        
        # Preprocess and convert to bag of words
        tokens = self.preprocess_text(question).split()
        bow = self.dictionary.doc2bow(tokens)
        topic_dist = self.model.get_document_topics(bow)
        
        if not topic_dist:
            return {
                "topic_id": None,
                "subcategory": "Unknown",
                "category": "Unknown",
                "distribution": []
            }
        
        # Get the topic with highest probability
        best_topic = max(topic_dist, key=lambda x: x[1])[0]
        
        # Get category information from mapping
        topic_info = self.topic_mapping.get(
            str(best_topic), 
            {"subcategory": "Unknown", "category": "Unknown"}
        )
        
        return {
            "topic_id": best_topic,
            "subcategory": topic_info["subcategory"],
            "category": topic_info["category"],
            "distribution": topic_dist
        }


# Global instance (will be initialized in pipeline)
lda_classifier = None

def get_lda_classifier():
    """Get the global LDA classifier instance."""
    return lda_classifier

def initialize_lda_classifier(model_path, dict_path, mapping_path):
    """Initialize the global LDA classifier."""
    global lda_classifier
    lda_classifier = LDAClassifier(model_path, dict_path, mapping_path)
    return lda_classifier

