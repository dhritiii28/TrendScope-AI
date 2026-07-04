from collections import defaultdict
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models import TopicSnapshot

BLACKLIST = {
    "is", "are", "was", "were",
    "be", "been", "being",

    "to", "of", "for", "on", "in", "at", "by", "with",
    "from", "after", "before", "into",

    "today", "latest", "breaking", "news",
    "daily", "live", "update",

    "best", "here", "there", "this", "that",
    "these", "those",

    "we", "you", "they", "he", "she", "it",

    "show", "shows", "showing",
    "want", "wants", "wanted",
    "say", "says", "said",

    "day", "days",
    "week", "weeks",
    "month", "months",
    "year", "years",

    "january", "february", "march", "april",
    "may", "june", "july", "august",
    "september", "october", "november", "december",

    "new", "more", "time",
    "people", "guest", "guests"
}


def generate_topic_snapshot(db: Session, category: str, trends):

    topic_data = defaultdict(list)

    for trend in trends:

        if not trend.keywords:
            continue

        topics = []

        for keyword in trend.keywords.split(","):

            keyword = keyword.strip().lower()

            if not keyword:
                continue

            if keyword in BLACKLIST:
                continue

            if keyword.isdigit():
                continue

            if len(keyword) < 3 and keyword not in {"ai", "us", "uk", "eu"}:
                continue

            topics.append(keyword)

        for topic in topics:
            topic_data[topic].append(trend)

    snapshot_count = 0

    for topic, articles in topic_data.items():

        total_score = 0
        positive = 0
        neutral = 0
        negative = 0

        for article in articles:

            total_score += article.trend_score or 0

            if article.sentiment == "Positive":
                positive += 1

            elif article.sentiment == "Neutral":
                neutral += 1

            else:
                negative += 1

        snapshot = TopicSnapshot(

            topic=topic,

            category=category,

            article_count=len(articles),

            avg_trend_score=total_score / len(articles),

            positive_articles=positive,

            neutral_articles=neutral,

            negative_articles=negative,

            captured_at=datetime.utcnow()

        )

        db.add(snapshot)

        snapshot_count += 1

    db.commit()

    return snapshot_count