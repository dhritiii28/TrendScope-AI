from datetime import datetime

from sqlalchemy.orm import Session

from backend.models import Trend

from backend.news_sources.aggregator import fetch_news

from backend.text_processing import clean_text
from backend.extraction import extract_keywords
from backend.sentiment_analysis import analyze_sentiment
from backend.trend_scoring import calculate_trend_score

from backend.topic_analysis.snapshot import generate_topic_snapshot


def collect_and_store_trends(
    db: Session,
    category: str,
    pages: int = 1
):
    """
    Fetch news, process articles, store trends,
    generate topic snapshots and return
    the number of newly added articles.
    """

    articles = fetch_news(category, pages)

    print(f"\n========== {category.upper()} ==========")
    print(f"Fetched {len(articles)} articles")

    count = 0

    new_trends = []

    for article in articles:

        existing_article = (
            db.query(Trend)
            .filter(Trend.url == article["url"])
            .first()
        )

        if existing_article:
            continue

        combined_text = (
            (article["title"] or "")
            + " "
            + (article["description"] or "")
        )

        cleaned = clean_text(combined_text)

        keywords = extract_keywords(combined_text)

        sentiment = analyze_sentiment(cleaned)

        trend_score = calculate_trend_score(
            sentiment,
            keywords,
            article["published_at"],
            article["source"]
        )

        trend = Trend(

            title=article["title"],

            description=article["description"],

            source=article["source"],

            published_at=article["published_at"],

            url=article["url"],

            cleaned_text=cleaned,

            keywords=keywords,

            sentiment=sentiment,

            trend_score=trend_score,

            category=category,

            collected_at=datetime.utcnow()

        )

        db.add(trend)

        db.flush()

        new_trends.append(trend)

        count += 1

    db.commit()

    snapshots = generate_topic_snapshot(
        db,
        category,
        new_trends
    )

    print(f"{snapshots} topic snapshots created.")

    print(f"{count} new articles stored.")

    return count