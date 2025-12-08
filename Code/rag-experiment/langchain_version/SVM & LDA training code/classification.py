import numpy as np
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.utils.class_weight import compute_class_weight
from sentence_transformers import SentenceTransformer
import joblib

class SecurityQuestionClassifier:
    def __init__(self, model_path=None):
        # Loading the text embedding model（MiniLM）
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.classifier = None
        self.label_map = None
        if model_path:
            self.load_model(model_path)

    def train(self, df, text_column=["title","question"], label_column="Label1"):
        texts = df[text_column].fillna("").agg(" ".join, axis=1).tolist()
        labels = df[label_column].values
        vectors = self.embedding_model.encode(texts, show_progress_bar=True)

        # Category weight calculation
        class_labels = np.unique(labels)
        weights = compute_class_weight(class_weight="balanced", classes=class_labels, y=labels)
        class_weight_dict = dict(zip(class_labels, weights))

        # Training an SVM classifier
        clf = LinearSVC(class_weight=class_weight_dict)
        clf.fit(vectors, labels)

        # Storage Model
        self.classifier = clf
        self.label_map = class_labels

    def predict(self, question_text):
        vec = self.embedding_model.encode([question_text])
        pred = self.classifier.predict(vec)
        return pred[0]

    def save_model(self, path="svm_classifier.joblib"):
        joblib.dump({
            "classifier": self.classifier,
            "label_map": self.label_map
        }, path)

    def load_model(self, path):
        data = joblib.load(path)
        self.classifier = data["classifier"]
        self.label_map = data["label_map"]
