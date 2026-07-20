from .gnews import fetch_from_gnews
from .newsdata import fetch_from_newsdata
from .rss import fetch_from_rss


def remove_duplicates(articles):

    seen_urls = set()
    unique_articles = []

    for article in articles:

        url = article.get("url")

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)
        unique_articles.append(article)

    return unique_articles


def fetch_news(category: str, pages: int = 1):

    articles = []

    print(f"\nFetching '{category}' articles from GNews...")
    gnews_articles = fetch_from_gnews(category, pages )
    print(f"GNews returned {len(gnews_articles)} articles.")

    print(f"\nFetching '{category}' articles from NewsData...")
    newsdata_articles = fetch_from_newsdata(category, pages)
    print(f"NewsData returned {len(newsdata_articles)} articles.")
    
    # Fetch from RSS
    rss_articles = fetch_from_rss(category)

    articles.extend(gnews_articles)
    articles.extend(newsdata_articles)
    articles.extend(rss_articles)

    print(f"\nTotal before removing duplicates: {len(articles)}")

    articles = remove_duplicates(articles)

    print(f"Total after removing duplicates: {len(articles)}")

    return articles