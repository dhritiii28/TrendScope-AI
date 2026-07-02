from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:Dhriti_2804@localhost/trendscope_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind = engine)

Base = declarative_base()

def get_db():
    
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()