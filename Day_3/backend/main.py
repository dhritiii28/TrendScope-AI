from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Welcome to TrendScope AI Backend"
    }
    
@app.get("/about")
def about():
    return {
        "project": "TrendScope AI",
        "version": "1.0",
        "technology": "FastAPI Backend"
    }