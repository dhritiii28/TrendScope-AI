from sqlalchemy.orm import Session

from backend.services.trend_services import collect_and_store_trends
from backend.ml.train import train_model

def run_pipeline(db: Session):

    categories = [

        "technology",

        "ai",

        "business",

        "sports",

        "gaming",

        "health",
        
        "science",
        
        "fashion",
        "makeup",
        "beauty",
        "skincare",
        "luxury",
        "crypto",
        "entertainment"

    ]

    total_new_articles = 0

    print("\n========== STARTING AUTOMATION ==========\n")

    for category in categories:

        print(f"Processing {category}...")

        count = collect_and_store_trends(

            db=db,

            category=category,

            pages=1

        )

        total_new_articles += count

    print("\n========== PIPELINE COMPLETE ==========")

    print(f"New Articles Added: {total_new_articles}")

    if total_new_articles > 0:

        print("\nNew data detected.")

        print("Retraining model...\n")

        train_model()

    else:

        print("\nNo new articles found.")

        print("Skipping model retraining.")

    return total_new_articles