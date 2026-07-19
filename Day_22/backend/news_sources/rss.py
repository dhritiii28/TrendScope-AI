import feedparser

from .config import RSS_FEEDS


def fetch_from_rss(category: str):
    """
    Fetch articles from RSS feeds for a given category.

    Returns:
        List of dictionaries in the same format as GNews and NewsData.
    """

    articles = []

    feeds = RSS_FEEDS.get(category.lower(), [])

    if not feeds:
        print(f"No RSS feeds configured for '{category}'")
        return articles

    for feed_url in feeds:

        try:
            feed = feedparser.parse(feed_url)

            # Skip broken or invalid feeds
            if hasattr(feed, "bozo") and feed.bozo:
                print(f"Skipping invalid feed: {feed_url}")
                continue

            source_name = feed.feed.get("title", "RSS Feed")

            for entry in feed.entries:

                article = {
                    "title": entry.get("title", ""),
                    "description": entry.get("summary", ""),
                    "source": source_name,
                    "published_at": entry.get("published", ""),
                    "url": entry.get("link", ""),
                    "provider": "RSS"
                }

                articles.append(article)

        except Exception as e:
            print(f"Error reading RSS feed {feed_url}: {e}")

    return articles