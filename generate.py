import os
from groq import Groq
from dotenv import load_dotenv
from retrieve import retrieve

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant that answers questions about CS course difficulty based ONLY on the student reviews and forum posts provided to you.

Rules you must follow:
1. Answer ONLY using information from the provided documents. Do not use your general training knowledge.
2. Always cite sources by their name (e.g. "According to r/uofu..." or "A student on r/csMajors said..."). Never say "Document 1" or "Document 2" — use the source name shown in brackets.
3. If the provided documents do not contain enough information to answer, say only: "I don't have enough information in my sources to answer that question." Do not explain why or narrate your reasoning.
4. Do not make up courses, universities, or opinions not in the documents.
5. Do not narrate your thought process. Just give the answer directly.
6. Keep answers concise and direct."""


def ask(question):
    """
    Full RAG pipeline: retrieve chunks → generate grounded answer → return answer + sources.
    """
    # Retrieve top-k chunks
    chunks = retrieve(question, k=6)

# Build context string from chunks
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Source: {chunk['source']} | University: {chunk['university']}]\n{chunk['text']}"
        )
    context = "\n\n".join(context_parts)

    # Build prompt
    user_prompt = f"""Here are the relevant student reviews:

{context}

Question: {question}

Answer using ONLY the reviews above. When citing a source, use its name (e.g. "According to r/csMajors..." or "A student on r/uofu said..."). Never say "Document 1" or "Document 2"."""

    # Call Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000,
        temperature=0.2
    )

    answer = response.choices[0].message.content

    # Collect unique sources
    sources = list({f"{c['source']} ({c['university']})" for c in chunks})

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(chunks)
    }


# ── Quick test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_questions = [
        "What CS courses do students at multiple universities agree are difficult?",
        "What advice do students give about which CS courses not to take at the same time?",
        "What is the best restaurant in Paris?",  # out-of-scope test
    ]

    for question in test_questions:
        print(f"\nQUESTION: {question}")
        print("=" * 60)
        result = ask(question)
        print(result["answer"])
        print(f"\nSources: {', '.join(result['sources'])}")
        print("-" * 60)