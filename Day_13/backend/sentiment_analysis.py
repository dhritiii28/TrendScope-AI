from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text.

    Parameters:
        text (str): The cleaned text to analyze.

    Returns:
        str: "Positive", "Neutral", or "Negative"
    """

    if not text:
        return "Neutral"

    # Get sentiment scores
    sentiment_scores = sia.polarity_scores(text)

    # Compound score ranges from -1 to +1
    compound_score = sentiment_scores["compound"]

    # Classify sentiment
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"