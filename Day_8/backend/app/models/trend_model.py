from sqlalchemy import Column, Integer, String
from app.database import Base

class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    platform = Column(String)
    popularity = Column(Integer)