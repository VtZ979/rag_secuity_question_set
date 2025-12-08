from typing import Dict, Any
from langchain_core.runnables import Runnable
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Try to find or download vader_lexicon, but handle network errors gracefully
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    try:
        # Try to download silently
        nltk.download("vader_lexicon", quiet=True)
    except Exception as e:
        # If download fails, print warning but continue
        # The analyzer will fail later if the data is truly missing, but at least we won't crash on startup
        print(f"[WARNING] Could not download NLTK vader_lexicon: {e}")
        print("[INFO] VADER sentiment analysis may not work properly without the lexicon")
    
    
class VaderSentimentAnalyzer(Runnable):
  
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def invoke(self, input: str) -> Dict[str, Any]:
        scores = self.analyzer.polarity_scores(input)
        # add label judgment
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