from pydantic import BaseModel

class UserRegister(BaseModel):
    
    id: int
    
    username: str
    
    email: str
    
    password: str
    
class UserLogin(BaseModel):
    
    email: str
    
    password: str
    
    