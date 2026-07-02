from sqlalchemy import Column, Integer, String, Text, Float

from database import Base

class User(Base):
    
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key = True, index = True)
    
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
    
    