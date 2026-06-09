import json
import os
import re

DOCUMENTS_DIR = "documents"
OUTPUT_DIR = "documents/clean"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Reddit JSON helpers ────────────────────────────────────────────────────────

def extract_reddit_comments(filepath, source_meta):
    """Load a Reddit JSON file and return a list of comment strings with metadata."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []

    # Original post
    try:
        post = data[0]["data"]["children"][0]["data"]
        title = post.get("title", "")
        body = post.get("selftext", "").strip()
        lines.append(f"[POST] {title}\n{body}" if body else f"[POST] {title}")
    except Exception:
        pass

    # Top-level comments
    try:
        for child in data[1]["data"]["children"]:
            body = child["data"].get("body", "").strip()
            if body and body not in ("[deleted]", "[removed]"):
                lines.append(body)
    except Exception:
        pass

    return lines


def clean_text(text):
    """Remove leftover HTML entities and extra whitespace."""
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&#39;", "'", text)
    text = re.sub(r"<[^>]+>", "", text)          # strip any stray HTML tags
    text = re.sub(r"\n{3,}", "\n\n", text)        # collapse blank lines
    text = text.strip()
    return text


# ── Source definitions ─────────────────────────────────────────────────────────

REDDIT_SOURCES = [
    {
        "filename": "omscs_difficulty.json",
        "output": "omscs_difficulty.txt",
        "university": "Georgia Tech",
        "subreddit": "r/OMSCS",
        "url": "https://www.reddit.com/r/OMSCS/comments/1hsbc76/all_courses_ranked_by_difficulty_2025_springfall/"
    },
    {
        "filename": "csmajors_hardest_undergrad.json",
        "output": "csmajors_hardest_undergrad.txt",
        "university": "Various",
        "subreddit": "r/csMajors",
        "url": "https://www.reddit.com/r/csMajors/comments/13u8utd/hardest_individual_undergrad_cs_course_in_the_us/"
    },
    {
        "filename": "rpi_cs_courses.json",
        "output": "rpi_cs_courses.txt",
        "university": "RPI",
        "subreddit": "r/RPI",
        "url": "https://www.reddit.com/r/RPI/comments/sfoxhy/calling_all_cs_major_to_give_your_opinion_of_the/"
    },
    {
        "filename": "yorku_cs_courses.json",
        "output": "yorku_cs_courses.txt",
        "university": "York University",
        "subreddit": "r/yorku",
        "url": "https://www.reddit.com/r/yorku/comments/i86cwl/computer_science_students_rank_your_undergrad/"
    },
    {
        "filename": "uml_easiest_hardest.json",
        "output": "uml_easiest_hardest.txt",
        "university": "UMass Lowell",
        "subreddit": "r/uml",
        "url": "https://www.reddit.com/r/uml/comments/d9ct6d/cs_required_classes_easiest_to_hardest/"
    },
    {
        "filename": "wgu_difficulty.json",
        "output": "wgu_difficulty.txt",
        "university": "WGU",
        "subreddit": "r/WGU_CompSci",
        "url": "https://www.reddit.com/r/WGU_CompSci/comments/13fovi2/class_difficulty_ranking/"
    },
    {
        "filename": "uofu_utah.json",
        "output": "uofu_utah.txt",
        "university": "University of Utah",
        "subreddit": "r/uofu",
        "url": "https://www.reddit.com/r/uofu/comments/vhi0bw/can_anyone_help_with_cs_course_planning_and_let/"
    },
    {
        "filename": "csmajors_hardest_subject.json",
        "output": "csmajors_hardest_subject.txt",
        "university": "Various",
        "subreddit": "r/csMajors",
        "url": "https://www.reddit.com/r/csMajors/comments/zrpwz4/in_your_own_opinion_what_is_the_hardest_subject/"
    },
]

TEXT_SOURCES = [
    {
        "filename": "omscentral_reviews.txt",
        "output": "omscentral_reviews.txt",
        "university": "Georgia Tech",
        "source": "OMSCentral",
        "url": "https://www.omscentral.com/"
    },
    {
        "filename": "ratemyprofessors.txt",
        "output": "ratemyprofessors.txt",
        "university": "UTRGV",
        "source": "Rate My Professors",
        "url": "https://www.ratemyprofessors.com/"
    },
]


# ── Process Reddit JSON files ──────────────────────────────────────────────────

for source in REDDIT_SOURCES:
    filepath = os.path.join(DOCUMENTS_DIR, source["filename"])
    if not os.path.exists(filepath):
        print(f"MISSING: {source['filename']} — skipping")
        continue

    print(f"Processing {source['filename']}...")
    comments = extract_reddit_comments(filepath, source)

    output_path = os.path.join(OUTPUT_DIR, source["output"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Source: {source['subreddit']}\n")
        f.write(f"University: {source['university']}\n")
        f.write(f"URL: {source['url']}\n")
        f.write("=" * 50 + "\n\n")
        for comment in comments:
            cleaned = clean_text(comment)
            if cleaned:
                f.write(cleaned + "\n\n---\n\n")

    print(f"  Saved {len(comments)} comments → {source['output']}")


# ── Process plain text files ───────────────────────────────────────────────────

for source in TEXT_SOURCES:
    filepath = os.path.join(DOCUMENTS_DIR, source["filename"])
    if not os.path.exists(filepath):
        print(f"MISSING: {source['filename']} — skipping")
        continue

    print(f"Processing {source['filename']}...")
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    cleaned = clean_text(raw)
    output_path = os.path.join(OUTPUT_DIR, source["output"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"  Cleaned and saved → {source['output']}")


print("\nDone! Clean files are in documents/clean/")