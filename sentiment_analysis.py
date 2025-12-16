# ============================================================
# 🧠 sentiment_analysis.py — Transformer-based Sentiment Analysis (Milestone 3+)
# ============================================================

from transformers import pipeline
from functools import lru_cache

# ------------------------------------------------------------
# Load the pre-trained model only once for speed
# ------------------------------------------------------------
@lru_cache(maxsize=1)
def load_sentiment_model():
    """
    Loads a RoBERTa-based model trained on social-media sentiment.
    Model labels:
      LABEL_0 → Negative
      LABEL_1 → Neutral
      LABEL_2 → Positive
    """
    print("🔍 Loading Transformer model for sentiment analysis (first time only)…")
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")


# ------------------------------------------------------------
# Analyze Sentiment
# ------------------------------------------------------------
def analyze_sentiment(text):
    """
    Analyzes sentiment using Hugging Face Transformers.
    Returns: 'Positive', 'Neutral', or 'Negative'
    """
    model = load_sentiment_model()
    try:
        # Limit text length to 512 tokens for safety
        result = model(text[:512])[0]
        label = result["label"]
        score = result["score"]

        # Convert model label to readable output
        if label == "LABEL_0":
            sentiment = "Negative"
        elif label == "LABEL_1":
            sentiment = "Neutral"
        else:
            sentiment = "Positive"

        print(f"✅ Transformer sentiment: {sentiment}  (confidence = {score:.2f})")
        return sentiment

    except Exception as e:
        print(f"❌ Sentiment analysis failed: {e}")
        return "Neutral"  # default fallback


# ------------------------------------------------------------
# Quick local test
# ------------------------------------------------------------
if __name__ == "__main__":
    samples = [
        "I absolutely love how technology is changing education!",
        "I'm worried automation will cause mass unemployment.",
        "The government released new AI policy guidelines today."
    ]
    for text in samples:
        print(f"\nText: {text}")
        sentiment = analyze_sentiment(text)
        print(f"Sentiment → {sentiment}")
