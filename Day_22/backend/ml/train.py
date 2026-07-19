import os
import joblib
import pandas as pd
import numpy as np

from backend.database import SessionLocal
from backend.models import TopicSnapshot

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

def train_model():
    
    # -------------------------------
    # Load Data
    # -------------------------------

    print("Loading TopicSnapshots...")

    db = SessionLocal()

    try:
        snapshots = db.query(TopicSnapshot).all()

        if len(snapshots) == 0:
            raise Exception("No snapshot data found.")

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

    print(f"\nLoaded {len(df)} snapshots.")

    # -------------------------------
    # Dataset Inspection
    # -------------------------------

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nDataset Info:")
    print(df.info())

    print("\nMissing Values:")
    print(df.isnull().sum())

    # -------------------------------
    # Sort chronologically
    # -------------------------------

    df = df.sort_values(["topic", "captured_at"])

    # -------------------------------
    # Create Future Target
    # -------------------------------

    df["future_score"] = (
        df.groupby("topic")["avg_trend_score"]
        .shift(-1)
    )

    print("\nFuture Score Preview:")
    print(
        df[
            [
                "topic",
                "avg_trend_score",
                "future_score"
            ]
        ].head(20)
    )

    # Remove only rows without a future target
    df = df.dropna(subset=["future_score"])

    print(f"\nRows after creating future target: {len(df)}")

    # -------------------------------
    # Features & Target
    # -------------------------------

    feature_columns = [
        "article_count",
        "avg_trend_score",
        "positive_articles",
        "neutral_articles",
        "negative_articles"
    ]

    X = df[feature_columns]
    y = df["future_score"]

    # -------------------------------   
    # Train-Test Split
    # -------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Testing samples : {len(X_test)}")

    # -------------------------------
    # Train Model
    # -------------------------------

    print("\nTraining Random Forest Model...")

    model = RandomForestRegressor(n_estimators=100,random_state=42,n_jobs=-1)

    model.fit(X_train, y_train)

    print("Model trained successfully.")

    # -------------------------------
    # Model Evaluation
    # -------------------------------

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print("\n========== MODEL PERFORMANCE ==========")
    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R²   : {r2:.4f}")

    # -------------------------------
    # Feature Importance
    # -------------------------------

    importance_df = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    )

    print("\n========== FEATURE IMPORTANCE ==========")
    print(importance_df)

    # -------------------------------
    # Save Model
    # -------------------------------

    os.makedirs("backend/ml/saved_models", exist_ok=True)

    model_path = "backend/ml/saved_models/trend_model.pkl"

    joblib.dump(model, model_path)

    print(f"\nModel saved successfully to:\n{model_path}")

    print(f"\nModel trained on {len(df)} historical transitions.")
    
if __name__ == "__main__":
    train_model()