import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "documents/chroma"
TOP_K = 6

# Load model and ChromaDB
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection("cs_difficulty")


def retrieve(query, k=TOP_K):
    """
    Takes a plain English query and returns the top-k most relevant chunks
    with their source metadata and distance scores.
    """
    embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=embedding,
        n_results=k
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "university": results["metadatas"][0][i]["university"],
            "filename": results["metadatas"][0][i]["filename"],
            "distance": round(results["distances"][0][i], 4)
        })
    return chunks


def print_results(query, chunks):
    print(f"\nQUERY: {query}")
    print("=" * 60)
    for i, chunk in enumerate(chunks):
        print(f"\nResult {i+1} | {chunk['source']} | {chunk['university']} | distance: {chunk['distance']}")
        print(chunk["text"][:300])
        print("-" * 40)


# ── Test with 3 evaluation questions ──────────────────────────────────────────

if __name__ == "__main__":
    test_queries = [
        "What CS courses do students at multiple universities agree are difficult?",
        "What advice do students give about which CS courses not to take at the same time?",
        "What factors besides course content make CS courses feel harder or easier?",
    ]

    for query in test_queries:
        chunks = retrieve(query)
        print_results(query, chunks)