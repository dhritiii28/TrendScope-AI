import os
import requests
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

DOMAINS = {
    "technology": "technology",
    "business": "business",
    "science": "science",
    "sports": "sports",
    "health": "health",
    "entertainment": "entertainment",
    "fashion": "fashion",
    "makeup": "makeup",
    "beauty": "beauty",
    "skincare": "skincare",
    "luxury": "luxury fashion",
    "gaming": "gaming",
    "ai": "artificial intelligence",
    "crypto": "cryptocurrency"
}


def fetch_news(category: str = "technology"):

    if category not in DOMAINS:
        print(f"Unsupported category: {category}")
        return []

    url = "https://gnews.io/api/v4/search"

    params = {
        "q": DOMAINS[category],
        "lang": "en",
        "country": "us",
        "max": 20,
        "apikey": GNEWS_API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    if response.status_code != 200:
        print(data)
        return []

    articles = data.get("articles", [])

    trend_list = []

    for article in articles:
        
        # Skip incomplete articles
        if not article.get("title") or not article.get("description"):
            continue

        trend = {
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt"),
            "url": article.get("url")
        }

        trend_list.append(trend)

    return trend_list