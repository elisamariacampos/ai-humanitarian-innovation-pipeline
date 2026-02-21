
"""
Humanitarian & Social Innovation RSS Tracker (Open Template)
=============================================================

This is a generic RSS aggregation pipeline designed for monitoring
social innovation, humanitarian impact, global development,
and public policy topics.

⚠️ This template does NOT contain:
- Private API keys
- Personal credentials
- Private spreadsheet IDs
- Restricted data sources

Users must configure their own credentials and spreadsheet ID.

Required packages:
    pip install feedparser google-auth google-auth-oauthlib google-api-python-client requests beautifulsoup4 lxml

"""

import feedparser
import datetime
import requests

# ─────────────────────────────────────────────
# CONFIGURATION (USER MUST EDIT)
# ─────────────────────────────────────────────

SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"
GOOGLE_CREDENTIALS_FILE = "credentials.json"

# ─────────────────────────────────────────────
# PUBLIC RSS SOURCES (Open & Permitted)
# ─────────────────────────────────────────────

FEEDS = [

    # Global Development & Policy
    {"name": "World Bank Blog", 
     "url": "https://blogs.worldbank.org/rss.xml", 
     "category": "Development"},

    {"name": "OECD Insights Blog", 
     "url": "https://oecdinsights.org/feed/", 
     "category": "Policy"},

    # Humanitarian & Global Affairs
    {"name": "ReliefWeb Updates", 
     "url": "https://reliefweb.int/updates/rss.xml", 
     "category": "Humanitarian"},

    # Innovation & Impact
    {"name": "Stanford Social Innovation Review", 
     "url": "https://ssir.org/site/rss", 
     "category": "Innovation"},

    {"name": "MIT Technology Review", 
     "url": "https://www.technologyreview.com/feed/", 
     "category": "Technology"},

    # Global News (Public RSS)
    {"name": "Reuters World News", 
     "url": "https://feeds.reuters.com/Reuters/worldNews", 
     "category": "Media"},

    {"name": "The Guardian Global Development", 
     "url": "https://www.theguardian.com/global-development/rss", 
     "category": "Media"},
]


# ─────────────────────────────────────────────
# RSS FETCH FUNCTION
# ─────────────────────────────────────────────

def fetch_feed(feed):
    print(f"Fetching: {feed['name']}")
    parsed = feedparser.parse(feed["url"])

    articles = []

    for entry in parsed.entries:
        article = {
            "source": feed["name"],
            "category": feed["category"],
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "fetched_at": datetime.datetime.utcnow().isoformat()
        }
        articles.append(article)

    return articles


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────

def run_pipeline():
    all_articles = []

    for feed in FEEDS:
        articles = fetch_feed(feed)
        all_articles.extend(articles)

    print(f"Total articles collected: {len(all_articles)}")
    return all_articles


if __name__ == "__main__":
    run_pipeline()
