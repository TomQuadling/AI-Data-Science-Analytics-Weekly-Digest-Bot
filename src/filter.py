import json
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path


INPUT_PATH = Path("data/raw/rss_items.json")
OUTPUT_PATH = Path("data/processed/filtered_items.json")

LOOKBACK_DAYS = 7

INCLUSION_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "ml",
    "data science",
    "analytics",
    "llm",
    "large language model",
    "copilot",
    "agent",
    "agentic",
    "automation",
    "forecast",
    "forecasting",
    "optimisation",
    "optimization",
    "decision-making",
    "decision making",
    "model",
    "models",
    "fraud detection",
    "productivity",
    "workflow",
    "workflows",
    "operations",
    "operational",
    "supply chain",
    "customer service",
    "marketing",
    "finance",
    "manufacturing",
    "warehouse",
    "clinical",
    "health",
    "governance",
    "regulation",
    "compliance",
]

EXCLUSION_KEYWORDS = [
    "the download",
    "top 5",
    "top 10",
    "7 essential",
    "beginner",
    "beginner’s guide",
    "beginner's guide",
    "sponsored",
    "how to become",
    "getting started",
    "free web apis",
    "website builders",
    "full stack",
    "quantum simulations",
    "quantum computing",
    "chip",
    "chips",
    "chipmaker",
    "semiconductor",
    "semiconductors",
    "processor",
    "processors",
    "gpu",
    "gpus",
    "data centre",
    "data centres",
    "data center",
    "data centers",
    "datacentre",
    "datacentres",
    "databricks blog rss",
    "funding haul",
    "ipo",
    "valuation",
    "retail investors",
    "investors",
    "satellite group",
    "starlink",
    "smart home",
    "carplay",
    "photo app",
    "robotaxi",
    "robotaxis",
    "stream deck",
    "website builder",
    "github repositories",
]

EXCLUSION_PATTERNS = [
    r"\btop\s+\d+\b",
    r"\b\d+\s+essential\b",
    r"\bbeginner'?s guide\b",
    r"\bgetting started\b",
]


def load_items(input_path: Path) -> list[dict]:
    """Load raw RSS items from JSON."""
    with input_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_items(items: list[dict], output_path: Path) -> None:
    """Save filtered items to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def parse_date(date_str: str | None) -> datetime | None:
    """Parse RSS date strings into timezone-aware datetimes."""
    if not date_str:
        return None

    try:
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        pass

    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def clean_text(text: str | None) -> str:
    """Clean HTML and normalise whitespace."""
    if not text:
        return ""

    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_boilerplate(summary: str) -> str:
    """Remove repeated feed boilerplate from summaries."""
    boilerplate_phrases = [
        "appeared first on",
        "the post",
    ]

    cleaned = summary
    lowered = cleaned.lower()

    for phrase in boilerplate_phrases:
        index = lowered.find(phrase)
        if index != -1:
            cleaned = cleaned[:index].strip()
            lowered = cleaned.lower()

    return cleaned.strip()


def is_recent(date_str: str | None, lookback_days: int = LOOKBACK_DAYS) -> bool:
    """Return True if item is within the lookback window."""
    published_dt = parse_date(date_str)
    if published_dt is None:
        return False

    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    return published_dt >= cutoff


def build_search_text(title: str | None, summary: str | None) -> str:
    """Combine title and summary into one lowercase string."""
    return f"{title or ''} {summary or ''}".lower().strip()


def is_excluded(search_text: str) -> bool:
    """Return True if item matches exclusion keywords or patterns."""
    if any(keyword in search_text for keyword in EXCLUSION_KEYWORDS):
        return True

    if any(re.search(pattern, search_text) for pattern in EXCLUSION_PATTERNS):
        return True

    return False


def is_relevant(search_text: str) -> bool:
    """Return True if item matches at least one inclusion keyword."""
    return any(keyword in search_text for keyword in INCLUSION_KEYWORDS)


def filter_items(items: list[dict]) -> list[dict]:
    """Apply recency, exclusion, and relevance filters."""
    filtered = []

    for item in items:
        cleaned_summary = clean_text(item.get("summary"))
        cleaned_summary = remove_boilerplate(cleaned_summary)
        search_text = build_search_text(item.get("title"), cleaned_summary)

        if not is_recent(item.get("published")):
            continue

        if is_excluded(search_text):
            continue

        if not is_relevant(search_text):
            continue

        cleaned_item = {
            "source": item.get("source"),
            "feed_url": item.get("feed_url"),
            "title": item.get("title"),
            "link": item.get("link"),
            "published": item.get("published"),
            "author": item.get("author"),
            "summary": cleaned_summary,
        }

        filtered.append(cleaned_item)

    return filtered


def main() -> None:
    print(f"Loading raw items from {INPUT_PATH}...")
    items = load_items(INPUT_PATH)
    print(f"Loaded {len(items)} items")

    filtered_items = filter_items(items)
    print(f"Kept {len(filtered_items)} relevant items from the last {LOOKBACK_DAYS} days")

    save_items(filtered_items, OUTPUT_PATH)
    print(f"Saved filtered items to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()