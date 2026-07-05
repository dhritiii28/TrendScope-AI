import os
import requests
from dotenv import load_dotenv

from .config import DOMAINS

load_dotenv()

NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")

# Categories natively supported by NewsData.io
NEWSDATA_NATIVE_CATEGORIES = {
    "technology",
    "business",
    "science",
    "sports",
    "health",
    "entertainment"
}


def fetch_from_newsdata(category: str, pages: int = 1):

    if category not in DOMAINS:
        return []

    url = "https://newsdata.io/api/1/latest?apikey=pub_3dc2c974a5424ec19f966d2832c5b4fb"

    params = {
        "apikey": NEWSDATA_API_KEY,
        "language": "en"
    }

    # Built-in NewsData categories
    if category in NEWSDATA_NATIVE_CATEGORIES:
        params["category"] = category

    # Custom searches
    else:
        params["q"] = DOMAINS[category]

    trend_list = []
    
    next_page = None
    
    for page in range(pages):

        if next_page:
            params["page"] = next_page

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("NewsData Error:", response.text)
            break

        data = response.json()

        articles = data.get("results", [])

        print(f"NewsData Page {page + 1}: {len(articles)} articles")

        for article in articles:

            if not article.get("title") or not article.get("description"):
                continue

            trend = {
                "title": article.get("title"),
                "description": article.get("description"),
                "source": article.get("source_id"),
                "published_at": article.get("pubDate"),
                "url": article.get("link"),
                "provider": "NewsData"
            }

            trend_list.append(trend)

        next_page = data.get("nextPage")

        if not next_page:
            break

    return trend_list