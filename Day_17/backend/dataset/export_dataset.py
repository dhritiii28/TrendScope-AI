import pandas as pd
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Trend


def export_dataset(output_path="trend_dataset.csv"):
    db: Session = SessionLocal()

    try:
        # Fetch all records
        trends = db.query(Trend).all()

        data = []

        for t in trends:
            data.append({
                "title": t.title,
                "cleaned_text": t.cleaned_text,
                "keywords": t.keywords,
                "sentiment": t.sentiment,
                "trend_score": t.trend_score,
                "published_at": t.published_at,
                "source": t.source
            })

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Optional: remove empty rows
        df = df.dropna(subset=["cleaned_text", "trend_score"])

        # Save CSV
        df.to_csv(output_path, index=False)

        print(f"Dataset exported successfully → {output_path}")
        print(f"Total rows: {len(df)}")

    finally:
        db.close()


if __name__ == "__main__":
    export_dataset()