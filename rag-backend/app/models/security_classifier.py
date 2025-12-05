"""
Security Question Classifier using SVM
"""
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.utils.class_weight import compute_class_weight
from sentence_transformers import SentenceTransformer
import joblib
from pathlib import Path


class SecurityQuestionClassifier:
    """
    Classifier for categorizing security-related questions using SVM.
    """
    
    def __init__(self, model_path=None):
        """
        Initialize the classifier.
        
        Args:
            model_path: Path to the saved classifier model
        """
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.classifier = None
        self.label_map = None
        
        if model_path:
            self.load_model(model_path)

    def train(self, df, text_column=["title", "original question"], label_column="Label1"):
        """
        Train the classifier on a dataset.
        
        Args:
            df: DataFrame with training data
            text_column: Column(s) containing text to classify
            label_column: Column containing labels
        """
        texts = df[text_column].fillna("").agg(" ".join, axis=1).tolist()
        labels = df[label_column].values
        vectors = self.embedding_model.encode(texts, show_progress_bar=True)
        
        # Compute class weights for balanced training
        weights = compute_class_weight(
            class_weight="balanced", 
            classes=np.unique(labels), 
            y=labels
        )
        
        clf = LinearSVC(class_weight=dict(zip(np.unique(labels), weights)))
        clf.fit(vectors, labels)
        
        self.classifier = clf
        self.label_map = np.unique(labels)

    def predict(self, text: str) -> str:
        """
        Predict the category of a question.
        
        Args:
            text: Question text to classify
            
        Returns:
            Predicted category label
        """
        if self.classifier is None:
            raise ValueError("Classifier not loaded. Please load a model first.")
        
        vec = self.embedding_model.encode([text])
        return self.classifier.predict(vec)[0]

    def save_model(self, path="svm_classifier.joblib"):
        """
        Save the trained model to disk.
        
        Args:
            path: Path to save the model
        """
        if self.classifier is None:
            raise ValueError("No model to save. Train or load a model first.")
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            "classifier": self.classifier,
            "label_map": self.label_map
        }, path)

    def load_model(self, path="svm_classifier.joblib"):
        """
        Load a saved model from disk.
        
        Args:
            path: Path to the saved model
        """
        data = joblib.load(path)
        self.classifier = data["classifier"]
        self.label_map = data["label_map"]

