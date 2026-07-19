# Categories supported by TrendScope AI
# config.py  is the single source of truth for supported domains.


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

# Categories directly supported by NewsData.io
#NEWSDATA_CATEGORIES = {
#    "technology",
 #   "business",
#    "science",
#    "sports",
#   "health",
 #   "entertainment"
  #  }
  
# RSS feeds categorized by topic

RSS_FEEDS = {

    "technology": [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://feeds.arstechnica.com/arstechnica/index"
    ],

    "business": [
        "https://www.cnbc.com/id/10001147/device/rss/rss.html",
        "https://www.marketwatch.com/rss/topstories",
        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"
    ],

    "science": [
        "https://www.sciencedaily.com/rss/top/science.xml",
        "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
        "https://feeds.nature.com/nature/rss/current"
    ],

    "health": [
        "https://www.medicalnewstoday.com/rss",
        "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
        "https://feeds.bbci.co.uk/news/health/rss.xml"
    ],

    "sports": [
        "https://www.espn.com/espn/rss/news",
        "https://feeds.bbci.co.uk/sport/rss.xml",
        "https://www.skysports.com/rss/12040"
    ],

    "entertainment": [
        "https://www.hollywoodreporter.com/feed/",
        "https://variety.com/feed/",
        "https://www.rollingstone.com/music/music-news/feed/"
    ],

    "general": [
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
    ],

    "gaming": [
        "https://www.ign.com/rss",
        "https://www.gamespot.com/feeds/mashup/",
        "https://www.pcgamer.com/rss/"
    ],

    "crypto": [
        "https://cointelegraph.com/rss",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://decrypt.co/feed"
    ],

    "ai": [
        "https://openai.com/news/rss.xml",
        "https://huggingface.co/blog/feed.xml",
        "https://deepmind.google/blog/rss.xml"
    ],

    "fashion": [
        "https://www.vogue.com/feed/rss",
        "https://fashionunited.com/rss-news",
        "https://www.businessoffashion.com/feed/"
    ],

    "beauty": [
        "https://www.allure.com/feed/rss",
        "https://www.beautyindependent.com/feed/",
        "https://www.byrdie.com/feed"
    ],

    "makeup": [
        "https://www.makeup.com/feed",
        "https://www.temptalia.com/feed/",
        "https://www.allure.com/feed/rss"
    ],

    "skincare": [
        "https://www.dermstore.com/blog/feed/",
        "https://www.paulaschoice.com/expert-advice/feed",
        "https://www.byrdie.com/feed"
    ],

    "luxury": [
        "https://robbreport.com/feed/",
        "https://wwd.com/feed/",
        "https://www.luxuo.com/feed"
    ]
}