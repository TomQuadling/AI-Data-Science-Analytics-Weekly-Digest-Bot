import json
from pathlib import Path


INPUT_PATH = Path("data/processed/deduplicated_items.json")
OUTPUT_PATH = Path("data/outputs/weekly_digest.md")

MAX_STORIES = 5


def load_items(input_path: Path) -> list[dict]:
    """Load deduplicated items from JSON."""
    with input_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_markdown(content: str, output_path: Path) -> None:
    """Save newsletter markdown to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        f.write(content)


def generate_intro(items: list[dict]) -> str:
    """Generate a simple one-line intro based on themes in the selected stories."""
    combined_text = " ".join(
        f"{item.get('title', '')} {item.get('summary', '')}".lower()
        for item in items
    )

    themes = []

    if any(word in combined_text for word in ["fraud", "risk", "compliance", "regulation"]):
        themes.append("risk and governance")

    if any(word in combined_text for word in ["warehouse", "manufacturing", "operations", "workflow"]):
        themes.append("operational use cases")

    if any(word in combined_text for word in ["health", "clinical", "medical"]):
        themes.append("healthcare adoption")

    if any(word in combined_text for word in ["agent", "agentic", "copilot"]):
        themes.append("emerging AI tooling")

    if not themes:
        return "This week’s digest highlights a mix of practical AI and analytics developments with business relevance."

    if len(themes) == 1:
        return f"This week’s digest highlights developments in {themes[0]}."
    if len(themes) == 2:
        return f"This week’s digest highlights developments in {themes[0]} and {themes[1]}."

    return (
        f"This week’s digest highlights developments in {themes[0]}, "
        f"{themes[1]}, and {themes[2]}."
    )


def generate_why_it_matters(item: dict) -> str:
    """Generate a simple 'why it matters' line using keyword-based heuristics."""
    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()

    if any(word in text for word in ["fraud", "risk", "compliance", "governance"]):
        return "Why it matters: this points to how AI could change risk management, controls, or regulated decision-making."

    if any(word in text for word in ["warehouse", "manufacturing", "operations", "workflow", "productivity"]):
        return "Why it matters: this is a practical example of AI improving operational efficiency in real workflows."

    if any(word in text for word in ["health", "clinical", "medical"]):
        return "Why it matters: healthcare remains one of the clearest tests of whether AI tools deliver real value in high-stakes settings."

    if any(word in text for word in ["agent", "agentic", "copilot"]):
        return "Why it matters: this signals how AI tools may increasingly shift from passive assistants to more active workflow support."

    if any(word in text for word in ["supply chain", "forecast", "demand planning"]):
        return "Why it matters: this has potential relevance for forecasting, planning, and supply chain decision-making."

    return "Why it matters: this is a potentially useful signal for how AI and analytics are affecting business practice."


def format_story(item: dict, index: int) -> str:
    """Format one story as markdown."""
    title = item.get("title", "Untitled")
    summary = item.get("summary", "No summary available.")
    link = item.get("link", "")
    source = item.get("source", "Unknown source")
    score = item.get("scores", {}).get("total_score", "N/A")

    why_it_matters = generate_why_it_matters(item)

    return (
        f"### {index}. {title}\n\n"
        f"**Source:** {source}  \n"
        f"**Score:** {score}  \n"
        f"**Summary:** {summary}  \n"
        f"**{why_it_matters}**  \n"
        f"**Link:** {link}\n"
    )


def build_newsletter(items: list[dict]) -> str:
    """Build the full markdown digest."""
    selected_items = items[:MAX_STORIES]
    intro = generate_intro(selected_items)

    content = [
        "# Weekly AI, Data Science & Advanced Analytics Digest\n",
        "## Top Stories\n",
        f"{intro}\n",
    ]

    for i, item in enumerate(selected_items, start=1):
        content.append(format_story(item, i))
        content.append("\n---\n")

    return "\n".join(content)


def main() -> None:
    print(f"Loading deduplicated items from {INPUT_PATH}...")
    items = load_items(INPUT_PATH)
    print(f"Loaded {len(items)} items")

    newsletter_markdown = build_newsletter(items)
    save_markdown(newsletter_markdown, OUTPUT_PATH)

    print(f"Saved newsletter draft to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()