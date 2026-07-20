from apscheduler.schedulers.background import BackgroundScheduler

from backend.database import SessionLocal
from backend.automation.pipeline import run_pipeline


scheduler = BackgroundScheduler()


def scheduled_pipeline():

    print("\n========== SCHEDULED PIPELINE STARTED ==========\n")

    db = SessionLocal()

    try:

        run_pipeline(db)

    finally:

        db.close()


def start_scheduler():

    scheduler.add_job(

        scheduled_pipeline,

        "interval",

        hours = 2,

        id="trend_pipeline",

        replace_existing=True

    )

    scheduler.start()

    print("\nScheduler started successfully.")

    print("Pipeline will run every 2 hours.")