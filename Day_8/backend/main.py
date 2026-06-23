from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.trend_model import Trend
from models import User, Base
from schemas import UserLogin, UserRegister
from auth import hash_password, verify_password, create_token
from database import declarative_base, SessionLocal, get_db, engine
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from auth import verify_token
from auth import get_current_user
from news_services import fetch_news

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


@app.get("/trends")
def get_trends():

    articles = fetch_news()

    return articles
    
@app.post("/register")
def register_user(user:UserRegister, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.username == user.username).first()
    
    if existing_user :
        raise HTTPException(status_code = 404, detail = "Username already exists")
    
    new_user = User(id = user.id, username = user.username, email = user.email, password = hash_password(user.password))
    
    db.add(new_user)
    
    db.commit()
    
    return{"message": "User Registered Successfully"}

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
    
