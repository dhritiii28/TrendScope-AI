import joblib
import pandas as pd

from backend.database import SessionLocal
from backend.models import TopicSnapshot


def predict_trends(limit=10):

    model = joblib.load("backend/ml/saved_models/trend_model.pkl")

    db = SessionLocal()

    snapshots = db.query(TopicSnapshot).all()

    data = []

    for s in snapshots:
        data.append({
            "topic": s.topic,
            "category": s.category,
            "article_count": s.article_count,
            "avg_trend_score": s.avg_trend_score,
            "positive_articles": s.positive_articles,
            "neutral_articles": s.neutral_articles,
            "negative_articles": s.negative_articles
        })

    df = pd.DataFrame(data)

    X = df[
        [
            "article_count",
            "avg_trend_score",
            "positive_articles",
            "neutral_articles",
            "negative_articles"
        ]
    ]

    df["predicted_score"] = model.predict(X)

    df = df.sort_values(
        by="predicted_score",
        ascending=False
    )

    return df[
        [
            "topic",
            "category",
            "predicted_score"
        ]
    ].head(limit).to_dict(orient="records")