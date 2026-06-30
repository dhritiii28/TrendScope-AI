from pydantic import BaseModel

class UserRegister(BaseModel):
    
    id: int
    
    username: str
    
    email: str
    
    password: str
    
class UserLogin(BaseModel):
    
    email: str
    
    password: str
    
class TrendResponse(BaseModel):
    
    title: str
    
    description: str  | None = None
    
    source: str  | None = None
    
    published_at: str  | None = None
    
    url: str   | None = None
    
    cleaned_text: str   | None = None

    class Config:
        from_attributes = True
    
    keywords: str | None = None
    
    sentiment: str | None = None
    
    trend_score: float | None = None