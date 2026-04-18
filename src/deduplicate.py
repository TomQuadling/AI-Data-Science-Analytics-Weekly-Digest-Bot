import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


INPUT_PATH = Path("data/processed/scored_items.json")
OUTPUT_PATH = Path("data/processed/deduplicated_items.json")

MAX_ITEMS_TO_KEEP = 10
SIMILARITY_THRESHOLD = 0.72
MAX_PER_SOURCE = 2
MAX_VENDOR_AUTHORED = 2
MAX_KDNUGGETS = 1
MAX_PUBLIC_SECTOR_HEAVY = 1
MIN_BUSINESS_USE_CASE_ITEMS = 2

VENDOR_AUTHORED_SOURCES = {
    "Azure Blog",
    "Databricks Blog",
    "AWS Machine Learning Blog",
    "AWS AI News Blog",
    "AWS Big Data Blog",
    "Google Cloud AI Blog",
    "Google Cloud Blog - Data Analytics",
    "Google AI Blog",
    "Power BI Blog",
    "Microsoft Industry Blog",
    "Microsoft SQL Server Blog",
}

PUBLIC_SECTOR_HEAVY_KEYWORDS = [
    "public sector",
    "government institutions",
    "government agency",
    "government agencies",
    "pentagon",
    "ministry",
    "defense",
    "defence",
]

BUSINESS_USE_CASE_PRIORITY_KEYWORDS = [
    "implemented",
    "deployed",
    "rolled out",
    "in production",
    "workflow",
    "operations",
    "business intelligence",
    "bi",
    "dashboard",
    "dashboards",
    "decision support",
    "enterprise analytics",
    "fraud detection",
    "supply chain",
    "manufacturing",
    "warehouse",
    "real-time",
]


def load_items(input_path: Path) -> list[dict]:
    with input_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_items(items: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def normalise_text(text: str | None) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_comparison_text(item: dict) -> str:
    title = normalise_text(item.get("title", ""))
    summary = normalise_text(item.get("summary", ""))
    return f"{title} {summary}".strip()


def text_similarity(text_a: str, text_b: str) -> float:
    return SequenceMatcher(None, text_a, text_b).ratio()


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def is_duplicate(candidate: dict, kept_items: list[dict]) -> bool:
    candidate_text = build_comparison_text(candidate)

    for kept_item in kept_items:
        kept_text = build_comparison_text(kept_item)
        similarity = text_similarity(candidate_text, kept_text)

        if similarity >= SIMILARITY_THRESHOLD:
            return True

    return False


def is_public_sector_heavy(item: dict) -> bool:
    text = build_comparison_text(item)
    return contains_any(text, PUBLIC_SECTOR_HEAVY_KEYWORDS)


def is_business_use_case_priority(item: dict) -> bool:
    text = build_comparison_text(item)
    return contains_any(text, BUSINESS_USE_CASE_PRIORITY_KEYWORDS)


def passes_diversity_rules(candidate: dict, kept_items: list[dict]) -> bool:
    source_counts = Counter(item.get("source", "") for item in kept_items)
    vendor_count = sum(
        1 for item in kept_items if item.get("source", "") in VENDOR_AUTHORED_SOURCES
    )
    kdnuggets_count = sum(
        1 for item in kept_items if item.get("source", "") == "KDnuggets"
    )
    public_sector_count = sum(
        1 for item in kept_items if is_public_sector_heavy(item)
    )

    candidate_source = candidate.get("source", "")

    if source_counts[candidate_source] >= MAX_PER_SOURCE:
        return False

    if candidate_source in VENDOR_AUTHORED_SOURCES and vendor_count >= MAX_VENDOR_AUTHORED:
        return False

    if candidate_source == "KDnuggets" and kdnuggets_count >= MAX_KDNUGGETS:
        return False

    if is_public_sector_heavy(candidate) and public_sector_count >= MAX_PUBLIC_SECTOR_HEAVY:
        return False

    return True


def deduplicate_items(items: list[dict]) -> list[dict]:
    unique_items = []

    # Pass 1: prioritise strong business use case / enterprise analytics items
    for item in items:
        if len(unique_items) >= MIN_BUSINESS_USE_CASE_ITEMS:
            break

        if not is_business_use_case_priority(item):
            continue

        if is_duplicate(item, unique_items):
            continue

        if not passes_diversity_rules(item, unique_items):
            continue

        unique_items.append(item)

    # Pass 2: fill remaining slots normally
    for item in items:
        if len(unique_items) >= MAX_ITEMS_TO_KEEP:
            break

        if is_duplicate(item, unique_items):
            continue

        if not passes_diversity_rules(item, unique_items):
            continue

        unique_items.append(item)

    return unique_items


def main() -> None:
    print(f"Loading scored items from {INPUT_PATH}...")
    items = load_items(INPUT_PATH)
    print(f"Loaded {len(items)} scored items")

    deduplicated_items = deduplicate_items(items)
    print(f"Kept {len(deduplicated_items)} unique items after deduplication")

    save_items(deduplicated_items, OUTPUT_PATH)
    print(f"Saved deduplicated items to {OUTPUT_PATH}")

    if deduplicated_items:
        print("\nTop unique stories:")
        for i, item in enumerate(deduplicated_items, start=1):
            score = item.get("scores", {}).get("total_score", "N/A")
            print(f"{i}. {item['title']} ({score})")


if __name__ == "__main__":
    main()