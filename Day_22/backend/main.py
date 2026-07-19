from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import User, Base, Trend
from backend.schemas import UserLogin, UserRegister, TrendResponse
from backend.auth import hash_password, verify_password, create_token
from backend.database import declarative_base, SessionLocal, get_db, engine
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from sqlalchemy import func, case
from fastapi.security import HTTPAuthorizationCredentials
from backend.auth import verify_token
from backend.auth import get_current_user
from backend.text_processing import clean_text
from backend.extraction import extract_keywords
from backend.sentiment_analysis import analyze_sentiment
from backend.trend_scoring import calculate_trend_score
import pandas as pd
import os
from backend.news_sources.aggregator import fetch_news
from backend.ml.predict import predict_trends
from datetime import datetime
from backend.services.trend_services import collect_and_store_trends
from backend.automation.pipeline import run_pipeline
from backend.automation.scheduler import start_scheduler

app = FastAPI()

security = HTTPBearer()

# Create database tables
Base.metadata.create_all(bind= engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "TrendScope AI Backend Running"
    }


@app.get("/trends/{category}")
def get_trends(category: str):

    articles = fetch_news(category)

    return articles
    
@app.post("/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):

    print("Received:", user)
    
    users = db.query(User).all()

    print("\n===== USERS IN DATABASE =====")

    for u in users:
        print(u.id, u.username, u.email)

    print("=============================\n")

    existing_username = db.query(User).filter(User.username == user.username).first()
    print("Existing username:", existing_username)

    existing_email = db.query(User).filter(User.email == user.email).first()
    print("Existing email:", existing_email)

    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "User Registered Successfully"}

@app.post("/login")
def login_user(user:UserLogin, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user is None: 
        raise HTTPException(status_code = 404, detail = "User not Found")
    
    # if exists then verify password
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code = 404, detail ="Invalid Password")
    
    token = create_token({"sub": user.email})
    
    return{"access_token" : token}
    


@app.delete("/delete_user/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": f"User '{username}' deleted successfully."
    }

@app.get("/dashboard")
def dashboard(current_user = Depends(get_current_user)):
    
    return{"message": "Welcome to Trendscope AI",
           "user": current_user}
 
@app.get("/profile")
def profile(
    current_user: str = Depends(get_current_user)
):

    return {
        "message": "Protected Route Access Granted",
        "user": current_user
    }
    
    
@app.post("/store_trends/{category}")
def store_trends(
    category: str,
    pages: int = 1,
    db: Session = Depends(get_db)
):

    count = collect_and_store_trends(
        db=db,
        category=category,
        pages=pages
    )

    return {

        "message": "Trends stored successfully",

        "new_trends_added": count

    }
    
    


@app.get("/category/{category}", response_model=list[TrendResponse])
def get_trends_by_category(category: str,db: Session = Depends(get_db)):
    trends = (db.query(Trend).filter(Trend.category == category).all())

    return trends


@app.get("/top_trends/{category}", response_model=list[TrendResponse])
def get_top_trends_by_category(category: str,limit: int = 10,db: Session = Depends(get_db)):

    trends = (db.query(Trend).filter(Trend.category == category).order_by(Trend.trend_score.desc()).limit(limit).all())

    return trends

@app.get("/all_trends")
def get_all_trends(db: Session = Depends(get_db)):

    trends = db.query(Trend).all()

    return trends

@app.get("/top_trends", response_model=list[TrendResponse])
def get_top_trends(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    trends = (
        db.query(Trend)
        .order_by(Trend.trend_score.desc())
        .limit(limit)
        .all()
    )

    return trends

from backend.news_sources.config import DOMAINS

@app.get("/search_trends")
def search_trends(query: str, db: Session = Depends(get_db)):

    results = ( db.query(Trend).filter(
        Trend.title.ilike(f"%{query}%") |
        Trend.category.ilike(f"%{query}%") |
        Trend.source.ilike(f"%{query}%") |
        Trend.keywords.ilike(f"%{query}%")
    )
    .order_by(Trend.collected_at.desc())
    .limit(10)
    .all()
)
    return results

@app.get("/domains")
def get_domains():
    return {
        "domains": list(DOMAINS.keys())
    }
    
@app.get("/predict_trends")
def get_predictions():

    return predict_trends()

@app.post("/run_pipeline")
def execute_pipeline(
    db: Session = Depends(get_db)):

    total = run_pipeline(db)

    return {

        "message": "Automation completed",

        "new_articles": total

    }
    
@app.on_event("startup")
def startup_event():

    start_scheduler()
    
@app.get("/category_stats")
def get_category_stats(db: Session = Depends(get_db)):

    stats = (

        db.query(

            Trend.category,

            func.count(Trend.id).label("articles"),

            func.avg(Trend.trend_score).label("avg_score")

        )

        .group_by(Trend.category)

        .all()

    )

    return [

        {

            "category": row.category,

            "articles": row.articles,

            "avg_score": round(row.avg_score, 2)

        }

        for row in stats

    ]
    
@app.get("/compare_categories")
def compare_categories(
    cat1: str,
    cat2: str,
    db: Session = Depends(get_db)
):

    categories = [cat1, cat2]

    results = (
        db.query(
            Trend.category,
            func.count(Trend.id).label("articles"),
            func.avg(Trend.trend_score).label("avg_score"),      
        )
        .filter(Trend.category.in_(categories))
        .group_by(Trend.category)
        .all()
    )

    # Get ML predictions
    predictions = predict_trends()

    prediction_lookup = {}

    for item in predictions:

        category = item["category"]

        prediction_lookup.setdefault(category, []).append(
            item["predicted_score"]
        )

    response = {}

    for row in results:

        predicted_scores = prediction_lookup.get(row.category, [])

        avg_predicted = (
            sum(predicted_scores) / len(predicted_scores)
            if predicted_scores else row.avg_score
        )

        response[row.category] = {

            "category": row.category,

            "articles": row.articles,

            "avg_score": round(row.avg_score, 2),

            "predicted_score": round(avg_predicted, 2),

            "growth": round(avg_predicted - row.avg_score, 2),
        }

    return response