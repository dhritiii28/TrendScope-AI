from datetime import datetime, timezone


# Source credibility scores
SOURCE_SCORES = {
    "BBC News": 20,
    "Reuters": 20,
    "TechCrunch": 18,
    "The Verge": 17,
    "CNN": 16,
    "CNBC": 16,
    "Forbes": 15,
    "Business Insider": 15,
}


def calculate_trend_score(sentiment, keywords, published_at, source):
    """
    Calculate a trend score out of 100.

    Factors:
    1. Sentiment
    2. Number of keywords
    3. Article recency
    4. Source credibility
    """

    score = 0

    # ----------------------------
    # 1. Sentiment Score (30)
    # ----------------------------
    if sentiment == "Positive":
        score += 30
    elif sentiment == "Neutral":
        score += 20
    else:
        score += 10

    # ----------------------------
    # 2. Keyword Score (25)
    # ----------------------------
    keyword_count = len(keywords.split(",")) if keywords else 0
    score += min(keyword_count * 5, 25)

    # ----------------------------
    # 3. Recency Score (25)
    # ----------------------------
    try:
        published_date = datetime.fromisoformat(
            published_at.replace("Z", "+00:00")
        )

        current_date = datetime.now(timezone.utc)

        days_old = (current_date - published_date).days

        if days_old == 0:
            score += 25
        elif days_old == 1:
            score += 20
        elif days_old == 2:
            score += 15
        elif days_old <= 7:
            score += 10
        else:
            score += 5

    except Exception:
        score += 5

    # ----------------------------
    # 4. Source Score (20)
    # ----------------------------
    score += SOURCE_SCORES.get(source, 10)

    return round(score, 2)