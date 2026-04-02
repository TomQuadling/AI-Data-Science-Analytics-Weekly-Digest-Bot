import json
import re
from difflib import SequenceMatcher
from pathlib import Path


INPUT_PATH = Path("data/processed/scored_items.json")
OUTPUT_PATH = Path("data/processed/deduplicated_items.json")

MAX_ITEMS_TO_KEEP = 10
SIMILARITY_THRESHOLD = 0.72


def load_items(input_path: Path) -> list[dict]:
    """Load scored items from JSON."""
    with input_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_items(items: list[dict], output_path: Path) -> None:
    """Save deduplicated items to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def normalise_text(text: str | None) -> str:
    """Lowercase and simplify text for comparison."""
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def build_comparison_text(item: dict) -> str:
    """Combine title and summary for duplicate detection."""
    title = normalise_text(item.get("title", ""))
    summary = normalise_text(item.get("summary", ""))
    return f"{title} {summary}".strip()


def text_similarity(text_a: str, text_b: str) -> float:
    """Return a rough similarity score between two texts."""
    return SequenceMatcher(None, text_a, text_b).ratio()


def is_duplicate(candidate: dict, kept_items: list[dict]) -> bool:
    """Check whether candidate is too similar to an already-kept item."""
    candidate_text = build_comparison_text(candidate)

    for kept_item in kept_items:
        kept_text = build_comparison_text(kept_item)
        similarity = text_similarity(candidate_text, kept_text)

        if similarity >= SIMILARITY_THRESHOLD:
            return True

    return False


def deduplicate_items(items: list[dict]) -> list[dict]:
    """
    Keep highest-scoring unique items.
    Assumes input is already sorted highest score first.
    """
    unique_items = []

    for item in items:
        if not is_duplicate(item, unique_items):
            unique_items.append(item)

        if len(unique_items) >= MAX_ITEMS_TO_KEEP:
            break

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