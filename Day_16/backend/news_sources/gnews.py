import os
import requests
from dotenv import load_dotenv

from .config import DOMAINS

load_dotenv()

GNEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_from_gnews(category: str, pages: int = 1):

    if category not in DOMAINS:
        return []

    url = "https://gnews.io/api/v4/search?q=technology&lang=en&max=5&apikey=5b01ea3a39c6e1f6cf722e69b6e4411a"

    params = {
        "q": DOMAINS[category],
        "lang": "en",
        "country": "us",
        "max": 20,
        "apikey": GNEWS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    articles = data.get("articles", [])

    trend_list = []

    for article in articles:

        if not article.get("title") or not article.get("description"):
            continue

        trend = {
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt"),
            "url": article.get("url"),
            "provider": "GNews"
        }

        trend_list.append(trend)

    return trend_list