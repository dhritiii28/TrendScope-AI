import joblib
import pandas as pd

from backend.database import SessionLocal
from backend.models import TopicSnapshot


def predict_trends():

    # Load trained model
    model = joblib.load("backend/ml/saved_models/trend_model.pkl")

    db = SessionLocal()

    try:
        snapshots = db.query(TopicSnapshot).all()

        if len(snapshots) == 0:
            return {
                "message": "No snapshot data found."
            }

        data = []

        for s in snapshots:
            data.append({
                "topic": s.topic,
                "category": s.category,
                "article_count": s.article_count,
                "avg_trend_score": s.avg_trend_score,
                "positive_articles": s.positive_articles,
                "neutral_articles": s.neutral_articles,
                "negative_articles": s.negative_articles,
                "captured_at": s.captured_at
            })

    finally:
        db.close()

    df = pd.DataFrame(data)

    # Keep only the latest snapshot for each topic
    df = (
        df.sort_values("captured_at")
          .groupby("topic", as_index=False)
          .last()
    )

    feature_columns = [
        "article_count",
        "avg_trend_score",
        "positive_articles",
        "neutral_articles",
        "negative_articles"
    ]

    X = df[feature_columns]

    df["predicted_score"] = model.predict(X)

    df = df.sort_values(
        by="predicted_score",
        ascending=False
    )

    print("\nTop Predicted Trending Topics\n")

    print(
        df[
            [
                "topic",
                "category",
                "predicted_score"
            ]
        ].head(10)
    )

    # Determine trend direction
    df["trend"] = df.apply(
        lambda row: (
            "Rising"
            if row["predicted_score"] > row["avg_trend_score"]
            else "Falling"
        ),
        axis=1
    )
    
    print("NEW PREDICT FILE IS RUNNING")
    
    print(df[[
        "topic",
        "category",
        "avg_trend_score",
        "predicted_score",
        "trend"
    ]].head())
    


    return (
        df[
            [
                "topic",
                "category",
                "avg_trend_score",
                "predicted_score",
                "trend"
            ]
        ]
        .rename(
            columns={
                "avg_trend_score": "current_score"
            }
        )
        .head(20)
        .to_dict(orient="records")
    )


if __name__ == "__main__":
    from pprint import pprint

    result = predict_trends()
    pprint(result)