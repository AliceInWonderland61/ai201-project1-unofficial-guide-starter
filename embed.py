import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "documents/chunks.json"
CHROMA_DIR = "documents/chroma"

# Load chunks
print("Loading chunks...")
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)
print(f"  {len(chunks)} chunks loaded")

# Load embedding model
print("Loading embedding model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("  Model loaded")

# Set up ChromaDB
print("Setting up ChromaDB...")
client = chromadb.PersistentClient(path=CHROMA_DIR)

# Delete existing collection if it exists (clean slate)
try:
    client.delete_collection("cs_difficulty")
except:
    pass

collection = client.create_collection("cs_difficulty")

# Embed and store in batches
print("Embedding and storing chunks...")
BATCH_SIZE = 50

for i in range(0, len(chunks), BATCH_SIZE):
    batch = chunks[i:i + BATCH_SIZE]
    
    texts = [c["text"] for c in batch]
    ids = [c["id"] for c in batch]
    metadatas = [
        {
            "source": c["source"],
            "university": c["university"],
            "filename": c["filename"]
        }
        for c in batch
    ]
    
    embeddings = model.encode(texts).tolist()
    
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    
    print(f"  Stored chunks {i+1} to {min(i+BATCH_SIZE, len(chunks))}")

print(f"\nDone! {collection.count()} chunks stored in ChromaDB")

# Quick verification test
print("\nVerification test — searching for 'hardest CS course'...")
results = collection.query(
    query_embeddings=model.encode(["hardest CS course"]).tolist(),
    n_results=3
)
for i, doc in enumerate(results["documents"][0]):
    meta = results["metadatas"][0][i]
    print(f"\nResult {i+1}: [{meta['source']} | {meta['university']}]")
    print(doc[:200])