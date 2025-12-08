import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 加载数据
file_path = "code/rag-backend/data/StackOverflow_security_sample_labelled_all.csv"
df = pd.read_csv(file_path)

# 初始化 VADER 情感分析器
sia = SentimentIntensityAnalyzer()


# 定义情感分析函数
def analyze_sentiment_vader(answer):
    sentiment_score = sia.polarity_scores(answer)

    # 通过 compound 值判断情感
    if sentiment_score["compound"] >= 0.05:
        return "positive"
    elif sentiment_score["compound"] <= -0.05:
        return "negative"
    else:
        return "neutral"


# sentiment analysis 'accepted answers' 列进行情感分析
df["sentiment"] = df["accepted answers"].apply(
    lambda x: analyze_sentiment_vader(str(x)) if isinstance(x, str) else "neutral"
)

# result of sentiment analysis
print(df[["accepted answers", "sentiment"]].head())

# distribution of sentiment analysis results
sentiment_counts = df["sentiment"].value_counts()

# Bar chart of sentiment distribution
plt.figure(figsize=(8, 6))
sentiment_counts.plot(kind="bar", color=["skyblue", "lightcoral", "lightgreen"])
plt.title("Sentiment Analysis Distribution of Accepted Answers")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.xticks(rotation=0)
plt.show()
