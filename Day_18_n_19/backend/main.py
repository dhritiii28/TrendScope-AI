from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import User, Base, Trend
from backend.schemas import UserLogin, UserRegister, TrendResponse
from backend.auth import hash_password, verify_password, create_token
from backend.database import declarative_base, SessionLocal, get_db, engine
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
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
def store_trends(category: str, 
                 pages: int = 1,  
                 db: Session = Depends(get_db)):
    
    articles = fetch_news(category, pages)
    
    print("Category received:", category)
    print("Number of articles:", len(articles))
    print("Articles:", articles)
    
    count = 0
    
    new_trends = []

    for article in articles:
        
        existing_article = db.query(Trend).filter(Trend.url == article["url"]).first()
        
        if not existing_article:
            combined_text = ((article["title"] or "")+ " "+ (article["description"] or ""))
            
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
                category = category,
                collected_at=datetime.utcnow()
            )
            
            
            
            
            db.add(trend)
            
            db.flush()
            
            new_trends.append(trend)
            
        
            count += 1

    db.commit()
    
    from backend.topic_analysis.snapshot import generate_topic_snapshot
    
    snapshots = generate_topic_snapshot(db, category, new_trends)
    
    print(f"{snapshots} topic snapshots created.")

    return {"message": "Trends stored successfully",
            "new_trends_added": count}


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

    results = db.query(Trend).filter(
        Trend.title.ilike(f"%{query}%") |
        Trend.category.ilike(f"%{query}%") |
        Trend.source.ilike(f"%{query}%") |
        Trend.keywords.ilike(f"%{query}%")
    ).limit(50).all()

    return results

@app.get("/domains")
def get_domains():
    return {
        "domains": list(DOMAINS.keys())
    }
    
@app.get("/predict_trends")
def get_predictions():

    return predict_trends()