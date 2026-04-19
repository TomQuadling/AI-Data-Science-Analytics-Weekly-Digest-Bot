# AI, Data Science & Advanced Analytics Weekly Digest Bot

## Objective

Build a weekly curated digest of AI, Data Science, and Advanced Analytics developments with a clear business lens.

The aim is to surface stories that help business and analytics professionals understand:
- where AI and advanced analytics are being applied in the real world
- which developments are likely to affect teams, tools, and decision-making
- what practical ideas, risks, and opportunities are worth paying attention to

The intended audience is business users with an interest in data and AI, rather than deeply technical practitioners.

---

## What We Built

This project produced a first working version of a rule-based pipeline that turns a large pool of AI, analytics, and business-tech stories into a short ranked shortlist.

The pipeline currently:
- collects stories from a broad set of RSS sources
- filters out low-value, off-topic, or overly biased content
- scores remaining stories against business relevance and practical usefulness
- deduplicates and applies diversity rules to improve shortlist quality
- creates a first draft markdown digest from the final shortlisted stories

In practice, this gives a repeatable way to move from a large news pool to a small set of candidate stories suitable for a weekly Teams-style digest.

---

## How We Built It

The project was built in Python as a sequence of simple pipeline steps:

1. **Collect**  
   Pull recent articles from selected RSS feeds.

2. **Filter**  
   Apply inclusion and exclusion logic to remove irrelevant stories, low-signal stories, and content outside the intended business focus.

3. **Score**  
   Rank stories using a rule-based scoring model that rewards business impact, practical application, signal strength, business use cases, and selected relevance bonuses.

4. **Deduplicate**  
   Remove near-duplicate stories and enforce shortlist diversity rules such as source limits and caps on overly biased/vendor-authored content.

5. **Summarise**  
   Produce a markdown draft digest from the shortlisted stories.

This version was intentionally built as a practical prototype first, with logic that is understandable and easy to refine before introducing LLM-based rewriting.

---

## Next Step / Project Status

The next phase of the project will move into a work environment rather than continue on this personal Git repository.

The likely direction is to rebuild or adapt the workflow in **Databricks**, where the shortlist generation and LLM-based rewrite step can be developed in a more production-ready environment.

That means:
- this repository represents the **personal prototype / proof of concept** phase
- future development will happen in a **work capacity**
- this Git repository is **not expected to be actively updated further**

The purpose of this repo is therefore to document the objective, approach, and first working version of the pipeline before the project transitions into a work-owned implementation.
