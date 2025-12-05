"""
Sentiment Analysis using VADER
"""
from typing import Dict, Any
from langchain_core.runnables import Runnable
import nltk

# Download VADER lexicon if not available
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

from nltk.sentiment import SentimentIntensityAnalyzer


class VaderSentimentAnalyzer(Runnable):
    """
    Sentiment analyzer using VADER (Valence Aware Dictionary and sEntiment Reasoner).
    """
    
    def __init__(self):
        """Initialize the VADER sentiment analyzer."""
        self.analyzer = SentimentIntensityAnalyzer()

    def invoke(self, input: str) -> Dict[str, Any]:
        """
        Analyze sentiment of input text.
        
        Args:
            input: Text to analyze
            
        Returns:
            Dictionary with sentiment label and scores
        """
        scores = self.analyzer.polarity_scores(input)
        
        # Determine sentiment label based on compound score
        label = (
            "positive" if scores["compound"] > 0.05 else
            "negative" if scores["compound"] < -0.05 else
            "neutral"
        )
        
        return {
            "text": input,
            "sentiment": label,
            "scores": scores
        }

