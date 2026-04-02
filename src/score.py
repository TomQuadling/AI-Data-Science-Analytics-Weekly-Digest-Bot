import json
from pathlib import Path


INPUT_PATH = Path("data/processed/filtered_items.json")
OUTPUT_PATH = Path("data/processed/scored_items.json")

MINIMUM_SCORE_THRESHOLD = 10

SOURCE_CREDIBILITY = {
    "FT Technology": 3,
    "MIT Technology Review": 3,
    "The Verge AI": 2,
    "Azure Blog": 2,
    "Databricks Blog": 2,
    "Towards Data Science": 1,
    "KDnuggets": 1,
}

BUSINESS_IMPACT_KEYWORDS = [
    "revenue",
    "sales",
    "profit",
    "profits",
    "margin",
    "margins",
    "cost",
    "costs",
    "efficiency",
    "efficient",
    "productivity",
    "customer",
    "customers",
    "customer service",
    "operations",
    "operational",
    "workflow",
    "workflows",
    "supply chain",
    "forecast",
    "forecasting",
    "decision",
    "decision-making",
    "decision making",
    "compliance",
    "risk",
    "risks",
    "growth",
    "performance",
    "fraud detection",
    "demand planning",
    "marketing",
    "finance",
    "manufacturing",
    "warehouse",
    "clinical",
]

PRACTICAL_APPLICATION_KEYWORDS = [
    "used",
    "use",
    "deployed",
    "deployment",
    "implemented",
    "implementation",
    "launched",
    "rolled out",
    "built",
    "building",
    "in production",
    "production",
    "adopted",
    "adoption",
    "workflow",
    "workflows",
    "tool",
    "tools",
    "platform",
    "system",
    "systems",
    "model that",
    "used ai to",
    "using ai to",
]

SIGNAL_STRENGTH_KEYWORDS = [
    "major",
    "launch",
    "launches",
    "partnership",
    "regulation",
    "regulatory",
    "shutdown",
    "failure",
    "risk",
    "warning",
    "transformation",
    "enterprise",
    "production",
    "breakthrough",
    "measurable",
    "speedup",
    "improved",
    "improvement",
    "rolled out",
    "in production",
]

BUSINESS_USE_CASE_KEYWORDS = [
    "used ai",
    "using ai",
    "implemented",
    "deployed",
    "rolled out",
    "in production",
    "customer service",
    "operations",
    "workflow",
    "fraud detection",
    "forecasting",
    "supply chain",
    "marketing",
    "finance",
    "manufacturing",
    "warehouse",
    "clinical",
]

FAILURE_RISK_KEYWORDS = [
    "risk",
    "risks",
    "failure",
    "failed",
    "backfired",
    "boycott",
    "ethical concerns",
    "shutdown",
    "shut down",
    "exposed",
    "crackdown",
    "wary",
    "warning",
]

REGULATION_KEYWORDS = [
    "regulation",
    "regulatory",
    "compliance",
    "law",
    "legal",
    "governance",
    "policy",
    "policies",
    "fda",
    "sovereignty",
]

THOUGHT_LEADERSHIP_KEYWORDS = [
    "what we need",
    "imperative",
    "future",
    "leadership",
    "should care",
    "how well do they work",
    "why",
]

TOOLING_PLATFORM_KEYWORDS = [
    "copilot",
    "azure",
    "databricks",
    "power bi",
    "fabric",
    "sql",
    "kubernetes",
    "gemini",
    "chatgpt",
    "claude",
    "llmops",
]

FMCG_KEYWORDS = [
    "fmcg",
    "consumer goods",
    "cpg",
    "food giant",
    "supermarket",
    "supermarkets",
    "grocery",
    "groceries",
    "retailer",
    "retailers",
    "unilever",
    "danone",
    "nestlé",
    "nestle",
    "pepsico",
    "coca-cola",
]

ADJACENT_INDUSTRY_KEYWORDS = [
    "retail",
    "retailer",
    "retailers",
    "supermarket",
    "supermarkets",
    "food",
    "healthcare",
    "pharma",
    "pharmaceutical",
    "manufacturing",
    "warehouse",
    "consumer",
    "clinical",
    "medical",
]

CORE_REGION_KEYWORDS = [
    "uk",
    "united kingdom",
    "britain",
    "british",
    "ireland",
    "irish",
    "nordic",
    "nordics",
    "baltic",
    "baltics",
    "europe",
    "european",
    "eu",
    "nhs",
]


def load_items(input_path: Path) -> list[dict]:
    """Load filtered items from JSON."""
    with input_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_items(items: list[dict], output_path: Path) -> None:
    """Save scored items to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def build_search_text(item: dict) -> str:
    """Combine title and summary into one lowercase string."""
    title = item.get("title", "") or ""
    summary = item.get("summary", "") or ""
    return f"{title} {summary}".lower()


def count_keyword_matches(text: str, keywords: list[str]) -> int:
    """Count how many keywords appear in the text."""
    return sum(1 for keyword in keywords if keyword in text)


def score_business_impact(text: str) -> int:
    """Score business impact out of 5."""
    matches = count_keyword_matches(text, BUSINESS_IMPACT_KEYWORDS)

    if matches >= 6:
        return 5
    if matches >= 4:
        return 4
    if matches >= 2:
        return 3
    if matches >= 1:
        return 2
    return 1


def score_practical_application(text: str) -> int:
    """Score practical application out of 4."""
    matches = count_keyword_matches(text, PRACTICAL_APPLICATION_KEYWORDS)

    if matches >= 5:
        return 4
    if matches >= 3:
        return 3
    if matches >= 1:
        return 2
    return 1


def score_signal_strength(text: str) -> int:
    """Score signal strength out of 4."""
    matches = count_keyword_matches(text, SIGNAL_STRENGTH_KEYWORDS)

    if matches >= 5:
        return 4
    if matches >= 3:
        return 3
    if matches >= 1:
        return 2
    return 1


def score_category_priority(text: str) -> int:
    """Score category priority out of 3 based on newsletter priorities."""
    if count_keyword_matches(text, BUSINESS_USE_CASE_KEYWORDS) >= 1:
        return 3

    if count_keyword_matches(text, FAILURE_RISK_KEYWORDS) >= 1:
        return 3

    if count_keyword_matches(text, REGULATION_KEYWORDS) >= 1:
        return 2

    if count_keyword_matches(text, THOUGHT_LEADERSHIP_KEYWORDS) >= 1:
        return 2

    if count_keyword_matches(text, TOOLING_PLATFORM_KEYWORDS) >= 1:
        return 1

    return 1


def score_source_credibility(source: str) -> int:
    """Get source credibility score out of 3."""
    return SOURCE_CREDIBILITY.get(source, 1)


def score_fmcg_bonus(text: str) -> int:
    """Return FMCG bonus."""
    return 2 if count_keyword_matches(text, FMCG_KEYWORDS) >= 1 else 0


def score_adjacent_industry_bonus(text: str) -> int:
    """Return adjacent industry bonus."""
    return 1 if count_keyword_matches(text, ADJACENT_INDUSTRY_KEYWORDS) >= 1 else 0


def score_core_region_bonus(text: str) -> int:
    """Return region bonus."""
    return 1 if count_keyword_matches(text, CORE_REGION_KEYWORDS) >= 1 else 0


def score_item(item: dict) -> dict:
    """Score one item and return an enriched dictionary."""
    text = build_search_text(item)

    business_impact = score_business_impact(text)
    practical_application = score_practical_application(text)
    signal_strength = score_signal_strength(text)
    category_priority = score_category_priority(text)
    source_credibility = score_source_credibility(item.get("source", ""))

    fmcg_bonus = score_fmcg_bonus(text)
    adjacent_industry_bonus = score_adjacent_industry_bonus(text)
    core_region_bonus = score_core_region_bonus(text)

    total_score = (
        business_impact
        + practical_application
        + signal_strength
        + category_priority
        + source_credibility
        + fmcg_bonus
        + adjacent_industry_bonus
        + core_region_bonus
    )

    scored_item = {
        **item,
        "scores": {
            "business_impact": business_impact,
            "practical_application": practical_application,
            "signal_strength": signal_strength,
            "category_priority": category_priority,
            "source_credibility": source_credibility,
            "fmcg_bonus": fmcg_bonus,
            "adjacent_industry_bonus": adjacent_industry_bonus,
            "core_region_bonus": core_region_bonus,
            "total_score": total_score,
        },
    }

    return scored_item


def score_items(items: list[dict]) -> list[dict]:
    """Score all items and keep only those above threshold."""
    scored_items = [score_item(item) for item in items]
    scored_items = [
        item
        for item in scored_items
        if item["scores"]["total_score"] >= MINIMUM_SCORE_THRESHOLD
    ]
    scored_items.sort(key=lambda item: item["scores"]["total_score"], reverse=True)
    return scored_items


def main() -> None:
    print(f"Loading filtered items from {INPUT_PATH}...")
    items = load_items(INPUT_PATH)
    print(f"Loaded {len(items)} filtered items")

    scored_items = score_items(items)
    print(
        f"Kept {len(scored_items)} scored items with total score >= {MINIMUM_SCORE_THRESHOLD}"
    )

    save_items(scored_items, OUTPUT_PATH)
    print(f"Saved scored items to {OUTPUT_PATH}")

    if scored_items:
        print("\nTop 10 stories:")
        for i, item in enumerate(scored_items[:10], start=1):
            print(f"{i}. {item['title']} ({item['scores']['total_score']})")


if __name__ == "__main__":
    main()