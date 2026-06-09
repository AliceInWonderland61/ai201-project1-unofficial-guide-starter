import os
import json

CLEAN_DIR = "documents/clean"
CHUNKS_FILE = "documents/chunks.json"

# ── Settings from planning.md ──────────────────────────────────────────────────
# Chunk size: 200-400 tokens (~150-300 words). We use characters as a proxy:
# 1 token ≈ 4 characters, so 300 tokens ≈ 1200 characters
CHUNK_SIZE_CHARS = 1200
OVERLAP_CHARS = 200   # ~50 tokens overlap

# ── Source metadata (used to tag every chunk) ─────────────────────────────────
SOURCE_META = {
    "omscs_difficulty.txt":          {"university": "Georgia Tech",     "source": "r/OMSCS"},
    "csmajors_hardest_undergrad.txt": {"university": "Various",         "source": "r/csMajors"},
    "rpi_cs_courses.txt":            {"university": "RPI",              "source": "r/RPI"},
    "yorku_cs_courses.txt":          {"university": "York University",  "source": "r/yorku"},
    "uml_easiest_hardest.txt":       {"university": "UMass Lowell",     "source": "r/uml"},
    "wgu_difficulty.txt":            {"university": "WGU",              "source": "r/WGU_CompSci"},
    "uofu_utah.txt":                 {"university": "University of Utah","source": "r/uofu"},
    "csmajors_hardest_subject.txt":  {"university": "Various",          "source": "r/csMajors"},
    "omscentral_reviews.txt":        {"university": "Georgia Tech",     "source": "OMSCentral"},
    "ratemyprofessors.txt":          {"university": "UTRGV",            "source": "Rate My Professors"},
}


def split_by_comment(text):
    """
    Split a Reddit-style document by the --- separator between comments.
    Each comment becomes one candidate chunk.
    """
    # Split on the separator we wrote in ingest.py
    parts = text.split("---")
    comments = []
    for part in parts:
        cleaned = part.strip()
        if len(cleaned) > 30:   # skip empty or near-empty splits
            comments.append(cleaned)
    return comments


def split_by_chars(text, chunk_size, overlap):
    """
    Fallback: split long text by character count with overlap.
    Used when a single comment is longer than CHUNK_SIZE_CHARS.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        # Try to end at a sentence boundary
        last_period = chunk.rfind(".")
        if last_period > chunk_size // 2:
            end = start + last_period + 1
            chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def chunk_document(filepath, filename):
    """
    Load one clean document and return a list of chunk dicts,
    each with text + metadata.
    """
    meta = SOURCE_META.get(filename, {"university": "Unknown", "source": "Unknown"})

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Skip the header lines (Source / University / URL / ===)
    if "=" * 10 in text:
        text = text.split("=" * 10, 1)[-1].strip()

    # Split by comment boundary first
    comment_blocks = split_by_comment(text)

    chunks = []
    for block in comment_blocks:
        if len(block) <= CHUNK_SIZE_CHARS:
            # Comment fits in one chunk — keep it whole
            chunks.append(block)
        else:
            # Comment is too long — split with overlap
            sub_chunks = split_by_chars(block, CHUNK_SIZE_CHARS, OVERLAP_CHARS)
            chunks.extend(sub_chunks)

    # Build chunk dicts with metadata
    chunk_dicts = []
    for i, chunk_text in enumerate(chunks):
        if chunk_text.strip():
            chunk_dicts.append({
                "id": f"{filename}_{i}",
                "text": chunk_text.strip(),
                "source": meta["source"],
                "university": meta["university"],
                "filename": filename,
            })

    return chunk_dicts


# ── Main ───────────────────────────────────────────────────────────────────────

all_chunks = []

if not os.path.exists(CLEAN_DIR):
    print(f"ERROR: {CLEAN_DIR} not found. Run ingest.py first.")
    exit(1)

for filename in os.listdir(CLEAN_DIR):
    if not filename.endswith(".txt"):
        continue
    filepath = os.path.join(CLEAN_DIR, filename)
    print(f"Chunking {filename}...")
    chunks = chunk_document(filepath, filename)
    all_chunks.extend(chunks)
    print(f"  {len(chunks)} chunks")

# Save all chunks to a JSON file
with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2, ensure_ascii=False)

print(f"\nTotal chunks: {len(all_chunks)}")
print(f"Saved to {CHUNKS_FILE}")

# ── Print 5 sample chunks for inspection ──────────────────────────────────────
print("\n" + "=" * 60)
print("SAMPLE CHUNKS (first 5)")
print("=" * 60)
for chunk in all_chunks[:5]:
    print(f"\nID: {chunk['id']}")
    print(f"Source: {chunk['source']} | University: {chunk['university']}")
    print(f"Length: {len(chunk['text'])} chars")
    print(f"Text:\n{chunk['text'][:400]}...")
    print("-" * 40)