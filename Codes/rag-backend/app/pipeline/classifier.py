import numpy as np
from sklearn.svm import LinearSVC
from sklearn.utils.class_weight import compute_class_weight
from sentence_transformers import SentenceTransformer
import joblib
import os
import warnings
import logging

# Ignore warnings and set offline mode for HuggingFace
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

# Set offline mode to disable network checks (model should already be cached locally)
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

class SecurityQuestionClassifier:
    def __init__(self, model_path=None):
        # Ensure offline mode is set before initializing model
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['HF_HUB_DISABLE_OFFLINE_WARNING'] = '1'
        
        # Initialize model with explicit cache directory to avoid network checks
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"[WARNING] Model initialization warning (may be network check): {e}")
            # Try again - model should be in cache
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.classifier = None
        self.label_map = None
        if model_path:
            self.load_model(model_path)

    def train(self, df, text_column=["title", "original question"], label_column="Label1"):
        texts = df[text_column].fillna("").agg(" ".join, axis=1).tolist()
        labels = df[label_column].values
        vectors = self.embedding_model.encode(texts, show_progress_bar=True)
        weights = compute_class_weight(class_weight="balanced", classes=np.unique(labels), y=labels)
        clf = LinearSVC(class_weight=dict(zip(np.unique(labels), weights)))
        clf.fit(vectors, labels)
        self.classifier = clf
        self.label_map = np.unique(labels)

    def predict(self, text: str) -> str:
        vec = self.embedding_model.encode([text])
        return self.classifier.predict(vec)[0]

    def save_model(self, path="svm_classifier.joblib"):
        joblib.dump({
            "classifier": self.classifier,
            "label_map": self.label_map
        }, path)

    def load_model(self, path="svm_classifier.joblib"):
        data = joblib.load(path)
        self.classifier = data["classifier"]
        self.label_map = data["label_map"]
