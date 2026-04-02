import json
from pathlib import Path

import feedparser


RSS_FEEDS = [
    {"name": "FT Technology", "url": "https://www.ft.com/technology?format=rss"},
    {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"},
    {"name": "Azure Blog", "url": "https://azure.microsoft.com/en-us/blog/feed/"},
    {"name": "Databricks Blog", "url": "https://www.databricks.com/blog/rss.xml"},
    {"name": "Towards Data Science", "url": "https://towardsdatascience.com/feed"},
    {"name": "KDnuggets", "url": "https://www.kdnuggets.com/feed"},
]


def parse_feed(feed_name: str, feed_url: str) -> list[dict]:
    """Parse one RSS feed and return a list of standardised article dictionaries."""
    parsed_feed = feedparser.parse(feed_url)
    items = []

    for entry in parsed_feed.entries:
        item = {
            "source": feed_name,
            "feed_url": feed_url,
            "title": getattr(entry, "title", None),
            "link": getattr(entry, "link", None),
            "published": getattr(entry, "published", None),
            "summary": getattr(entry, "summary", None),
            "author": getattr(entry, "author", None),
        }
        items.append(item)

    return items


def save_items(items: list[dict], output_path: Path) -> None:
    """Save collected items to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def main() -> None:
    all_items = []

    for feed in RSS_FEEDS:
        print(f"Collecting from: {feed['name']}")
        items = parse_feed(feed["name"], feed["url"])
        print(f"  Found {len(items)} items")
        all_items.extend(items)

    output_path = Path("data/raw/rss_items.json")
    save_items(all_items, output_path)

    print(f"\nDone. Saved {len(all_items)} items to {output_path}")


if __name__ == "__main__":
    main()