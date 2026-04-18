import json
from pathlib import Path


INPUT_PATH = Path("data/processed/filtered_items.json")
OUTPUT_PATH = Path("data/processed/scored_items.json")

MINIMUM_SCORE_THRESHOLD = 10

SOURCE_CREDIBILITY = {
    "FT Technology": 3,
    "FT Big Data": 3,
    "MIT Technology Review": 3,
    "McKinsey Insights": 3,
    "CIO": 2,
    "VentureBeat AI": 2,
    "The Verge AI": 2,

    # Credible but biased / vendor-authored
    "Azure Blog": 1,
    "Databricks Blog": 1,
    "AWS Machine Learning Blog": 1,
    "AWS AI News Blog": 1,
    "AWS Big Data Blog": 1,
    "Google Cloud AI Blog": 1,
    "Google Cloud Blog - Data Analytics": 1,
    "Google AI Blog": 1,
    "Power BI Blog": 1,
    "Microsoft Industry Blog": 1,
    "Microsoft SQL Server Blog": 1,

    # Mixed practitioner sources
    "Towards Data Science": 1,
    "KDnuggets": 1,
}

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

BUSINESS_IMPACT_KEYWORDS = [
    "revenue", "sales", "profit", "profits", "margin", "margins",
    "cost", "costs", "efficiency", "efficient", "productivity",
    "customer", "customers", "customer service",
    "operations", "operational", "workflow", "workflows",
    "supply chain", "forecast", "forecasting",
    "decision", "decision-making", "decision making",
    "compliance", "risk", "risks", "growth", "performance",
    "fraud detection", "demand planning", "marketing", "sales planning",
    "finance", "pricing", "procurement", "manufacturing",
    "warehouse", "clinical", "quality", "validation",
    "business process", "reporting", "dashboard", "kpi", "kpis",
]

PRACTICAL_APPLICATION_KEYWORDS = [
    "used", "use", "deployed", "deployment", "implemented", "implementation",
    "launched", "rolled out", "built", "building", "in production",
    "production", "adopted", "adoption", "workflow", "workflows",
    "tool", "tools", "platform", "system", "systems", "process",
    "automated", "automation", "reusable", "weekly", "replaced",
    "validation", "quality checks",
]

SIGNAL_STRENGTH_KEYWORDS = [
    "major", "launch", "launches", "partnership", "regulation", "regulatory",
    "shutdown", "failure", "risk", "warning", "transformation", "enterprise",
    "production", "breakthrough", "measurable", "speedup", "improved",
    "improvement", "rolled out", "in production", "operationalize",
    "operationalise", "scaled", "scale",
]

BUSINESS_USE_CASE_KEYWORDS = [
    "used ai", "using ai", "implemented", "deployed", "rolled out",
    "in production", "customer service", "operations", "workflow",
    "fraud detection", "forecasting", "supply chain", "marketing", "sales",
    "finance", "pricing", "procurement", "manufacturing", "warehouse",
    "clinical", "quality checks", "validation", "reporting", "dashboard",
    "business process",
]

FAILURE_RISK_KEYWORDS = [
    "risk", "risks", "failure", "failed", "backfired", "boycott",
    "ethical concerns", "shutdown", "shut down", "exposed",
    "crackdown", "wary", "warning",
]

REGULATION_KEYWORDS = [
    "regulation", "regulatory", "compliance", "law", "legal",
    "governance", "policy", "policies", "fda", "sovereignty",
    "eu ai act", "european commission",
]

THOUGHT_LEADERSHIP_KEYWORDS = [
    "what we need", "imperative", "future", "leadership",
    "should care", "how well do they work", "lessons",
    "playbook", "teaming",
]

TOOLING_PLATFORM_KEYWORDS = [
    "copilot", "azure", "databricks", "power bi", "fabric", "sql",
    "gemini", "chatgpt", "claude", "llmops", "vertex ai", "bedrock", "sagemaker",
]

BUSINESS_UPSKILLING_KEYWORDS = [
    "reusable ai workflow", "reusable workflow", "quality checks",
    "validation", "workflow", "weekly", "habit", "process",
    "operational efficiency", "teaming", "productivity",
    "applied to work", "real workflows",
]

MEASURABLE_OUTCOME_KEYWORDS = [
    "reduced", "reduction", "improved", "increase", "increased",
    "decrease", "decreased", "faster", "speedup", "boosted",
    "optimise", "optimize", "saved", "saving", "33×", "10x",
]

COMPANY_IMPLEMENTATION_KEYWORDS = [
    "company", "companies", "business", "businesses", "customer",
    "customers", "organization", "organisation", "retailer",
    "retailers", "hospital", "manufacturer", "enterprise",
]

FMCG_KEYWORDS = [
    "fmcg", "consumer goods", "cpg", "food giant", "supermarket",
    "supermarkets", "grocery", "groceries", "retailer", "retailers",
    "unilever", "danone", "nestlé", "nestle", "pepsico", "coca-cola",
]

ADJACENT_INDUSTRY_KEYWORDS = [
    "retail", "retailer", "retailers", "supermarket", "supermarkets",
    "food", "healthcare", "pharma", "pharmaceutical", "manufacturing",
    "warehouse", "consumer", "clinical", "medical",
]

CORE_REGION_KEYWORDS = [
    "uk", "united kingdom", "britain", "british", "ireland", "irish",
    "nordic", "nordics", "baltic", "baltics", "europe", "european", "eu", "nhs",
]

VENDOR_PROMO_KEYWORDS = [
    "weekly roundup", "week in review", "roundup", "and more", "preview",
    "best practices", "get started", "getting started", "amazon bedrock",
    "sagemaker", "agent registry", "aws generative ai services",
    "vertex ai", "fabric", "copilot",
]

PUBLIC_SECTOR_HEAVY_KEYWORDS = [
    "public sector", "government institutions", "government agency",
    "government agencies", "pentagon", "ministry", "defense", "defence",
]

BUSINESS_TRANSFERABLE_KEYWORDS = [
    "operations", "workflow", "compliance", "governance", "regulated industries",
    "risk", "productivity", "cost", "efficiency", "deployment", "production",
    "enterprise", "businesses", "companies",
]


def load_items(input_path: Path) -> list[dict]:
    with input_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_items(items: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def build_search_text(item: dict) -> str:
    title = item.get("title", "") or ""
    summary = item.get("summary", "") or ""
    return f"{title} {summary}".lower()


def count_keyword_matches(text: str, keywords: list[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def score_business_impact(text: str) -> int:
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
    matches = count_keyword_matches(text, PRACTICAL_APPLICATION_KEYWORDS)
    if matches >= 5:
        return 4
    if matches >= 3:
        return 3
    if matches >= 1:
        return 2
    return 1


def score_signal_strength(text: str) -> int:
    matches = count_keyword_matches(text, SIGNAL_STRENGTH_KEYWORDS)
    if matches >= 5:
        return 4
    if matches >= 3:
        return 3
    if matches >= 1:
        return 2
    return 1


def score_category_priority(text: str) -> int:
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
    return SOURCE_CREDIBILITY.get(source, 1)


def score_fmcg_bonus(text: str) -> int:
    return 2 if count_keyword_matches(text, FMCG_KEYWORDS) >= 1 else 0


def score_adjacent_industry_bonus(text: str) -> int:
    return 1 if count_keyword_matches(text, ADJACENT_INDUSTRY_KEYWORDS) >= 1 else 0


def score_core_region_bonus(text: str) -> int:
    return 1 if count_keyword_matches(text, CORE_REGION_KEYWORDS) >= 1 else 0


def score_business_upskilling_bonus(text: str) -> int:
    return 1 if count_keyword_matches(text, BUSINESS_UPSKILLING_KEYWORDS) >= 2 else 0


def score_measurable_outcome_bonus(text: str) -> int:
    return 1 if count_keyword_matches(text, MEASURABLE_OUTCOME_KEYWORDS) >= 2 else 0


def score_company_implementation_bonus(text: str) -> int:
    has_company_signal = contains_any(text, COMPANY_IMPLEMENTATION_KEYWORDS)
    has_use_case_signal = contains_any(text, BUSINESS_USE_CASE_KEYWORDS)
    return 1 if has_company_signal and has_use_case_signal else 0


def apply_source_specific_adjustments(item: dict, total_score: int, text: str) -> int:
    source = item.get("source", "")

    if source in {"Towards Data Science", "KDnuggets"}:
        business_matches = count_keyword_matches(text, BUSINESS_IMPACT_KEYWORDS)
        use_case_matches = count_keyword_matches(text, BUSINESS_USE_CASE_KEYWORDS)
        if business_matches == 0 and use_case_matches == 0:
            total_score -= 2

    if source in VENDOR_AUTHORED_SOURCES:
        total_score -= 1

    promo_matches = count_keyword_matches(text, VENDOR_PROMO_KEYWORDS)
    if promo_matches >= 2:
        total_score -= 2
    elif promo_matches == 1:
        total_score -= 1

    if contains_any(text, PUBLIC_SECTOR_HEAVY_KEYWORDS):
        if not contains_any(text, BUSINESS_TRANSFERABLE_KEYWORDS):
            total_score -= 3
        else:
            total_score -= 1

    return total_score


def score_item(item: dict) -> dict:
    text = build_search_text(item)

    business_impact = score_business_impact(text)
    practical_application = score_practical_application(text)
    signal_strength = score_signal_strength(text)
    category_priority = score_category_priority(text)
    source_credibility = score_source_credibility(item.get("source", ""))

    fmcg_bonus = score_fmcg_bonus(text)
    adjacent_industry_bonus = score_adjacent_industry_bonus(text)
    core_region_bonus = score_core_region_bonus(text)
    business_upskilling_bonus = score_business_upskilling_bonus(text)
    measurable_outcome_bonus = score_measurable_outcome_bonus(text)
    company_implementation_bonus = score_company_implementation_bonus(text)

    total_score = (
        business_impact
        + practical_application
        + signal_strength
        + category_priority
        + source_credibility
        + fmcg_bonus
        + adjacent_industry_bonus
        + core_region_bonus
        + business_upskilling_bonus
        + measurable_outcome_bonus
        + company_implementation_bonus
    )

    total_score = apply_source_specific_adjustments(item, total_score, text)

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
            "business_upskilling_bonus": business_upskilling_bonus,
            "measurable_outcome_bonus": measurable_outcome_bonus,
            "company_implementation_bonus": company_implementation_bonus,
            "total_score": total_score,
        },
    }

    return scored_item


def score_items(items: list[dict]) -> list[dict]:
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