from collections import defaultdict
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models import TopicSnapshot


def generate_topic_snapshot(db: Session, category: str, trends):

    topic_data = defaultdict(list)

    for trend in trends:

        if not trend.keywords:
            continue

        topics = [
            keyword.strip().lower()
            for keyword in trend.keywords.split(",")
            if keyword.strip()
        ]

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