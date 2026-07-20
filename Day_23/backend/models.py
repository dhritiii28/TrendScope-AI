from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime

from backend.database import Base

class User(Base):
    
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    
    username = Column(String, unique = True)
    
    email = Column(String, unique = True)
    
    password = Column(String)
    
class Trend(Base):

    __tablename__ = "Trends"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text)

    source = Column(String)

    published_at = Column(String)

    url = Column(String)
    
    cleaned_text = Column(Text)
    
    keywords = Column(Text)
    
    sentiment = Column(String(20))
    
    trend_score = Column(Float)
    
    category = Column(String(50))
    
    collected_at = Column(DateTime, default=datetime.utcnow)
    
    
class TopicSnapshot(Base):

    __tablename__ = "TopicSnapshots"

    id = Column(Integer, primary_key=True, index=True)

    topic = Column(String(200), nullable=False)

    category = Column(String(50))

    collected_at = Column(DateTime, default=datetime.utcnow)

    article_count = Column(Integer)

    avg_trend_score = Column(Float)

    positive_articles = Column(Integer)

    neutral_articles = Column(Integer)

    negative_articles = Column(Integer)
    
    captured_at = Column(DateTime, default=datetime.utcnow)