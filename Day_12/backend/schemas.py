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
    
    description: str
    
    source: str
    
    published_at: str
    
    url: str
    
    cleaned_text: str

    class Config:
        from_attributes = True
    
    keywords: str | None = None
    
    sentiment: str | None = None