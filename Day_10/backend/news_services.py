import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news():

    url = (
        "https://newsapi.org/v2/top-headlines"
        "?country=us"
        "&category=technology"
        f"&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    articles = data["articles"]

    trend_list = []

    for article in articles:

        trend = {
            "title": article["title"],
            "description": article["description"],
            "source": article["source"]["name"],
            "published_at": article["publishedAt"],
            "url": article["url"]
        }

        trend_list.append(trend)

    return trend_list