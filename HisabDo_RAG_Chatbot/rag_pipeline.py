"""
RAG Pipeline (RAG Pipeline, Stage 5)
Abbas's responsibility: RAG pipeline (retrieval portion)

"""

import os
from document_loader import load_documents
from chunker import chunk_all_documents
from embedder import ChunkEmbedder
from vector_store import VectorStore
# load the env variables from .env file
from dotenv import load_dotenv
load_dotenv()
import os

GORQ_API_KEY = os.getenv("GROQ_API_KEY")

class RAGPipeline:
    def __init__(self, knowledge_base_dir):
        self.knowledge_base_dir = knowledge_base_dir
        self.embedder = ChunkEmbedder()
        self.store = None
        self.chunks = None

    def build_index(self):
        """
        Runs the full ingestion pipeline once: load documents, clean,
        chunk, embed, and build the FAISS index. This is the
        "preparation" phase - done once, ahead of any user queries.
        """
        raw_docs = load_documents(self.knowledge_base_dir)
        self.chunks = chunk_all_documents(raw_docs)

        embeddings = self.embedder.fit_transform(self.chunks)

        self.store = VectorStore(embedding_dim=embeddings.shape[1])
        self.store.build(self.chunks, embeddings)

        return {
            "documents_loaded": len(raw_docs),
            "chunks_created": len(self.chunks),
            "vectors_indexed": self.store.total_vectors,
        }

    def retrieve(self, query, top_k=3):
        """
        The core retrieval step: given a user query, returns the top_k
        most relevant chunks with their similarity scores.

        This is the boundary of Abbas's responsibility per the team's
        role split (Section 9's diagram: retrieval ends at "Top Relevant
        Chunks", before "LLM Prompt").
        """
        if self.store is None:
            raise RuntimeError("Index not built yet. Call build_index() first.")

        query_embedding = self.embedder.transform(query)
        results = self.store.search(query_embedding, top_k=top_k)

        return [
            {
                "chunk_id": chunk.chunk_id,
                "section_title": chunk.section_title,
                "text": chunk.text,
                "category": chunk.source_category,
                "similarity_score": round(score, 4),
            }
            for chunk, score in results
        ]

    def generate_answer(self, query, top_k=3):
        """
        Full end-to-end demo: retrieval + LLM generation, matching
        Section 9's complete diagram. Included for demo completeness at
        Abbas's request - the LLM call itself is Omesha's responsibility
        area, reused here via the same Groq pattern from Day 10.

        Returns the retrieved chunks alongside the generated answer, so
        it's always clear which part came from verified retrieval vs.
        LLM-generated text (this also reflects the architecture
        document's anti-hallucination principle in Section 24).
        """
        retrieved_chunks = self.retrieve(query, top_k=top_k)

        if not retrieved_chunks:
            return {
                "query": query,
                "retrieved_chunks": [],
                "answer": "I couldn't find relevant information in the HisabDo knowledge base for that question.",
                "generated_by_llm": False,
            }

        context = "\n\n".join(
            f"[{c['section_title']}]\n{c['text']}" for c in retrieved_chunks
        )

        api_key = GORQ_API_KEY
        if not api_key:
            return {
                "query": query,
                "retrieved_chunks": retrieved_chunks,
                "answer": retrieved_chunks[0]["text"],
                "generated_by_llm": False,
                "note": "GROQ_API_KEY not set - returning the top retrieved chunk directly instead of an LLM-generated answer.",
            }

        from groq import Groq
        client = Groq(api_key=api_key)

        system_prompt = (
            "You are the HisabDo Assistant. Answer the user's question using ONLY "
            "the context below, which comes from HisabDo's official documentation. "
            "If the context doesn't fully answer the question, say so rather than "
            "making up details. Keep the answer short and practical.\n\n"
            f"Context:\n{context}"
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0.3,
            max_tokens=250,
        )

        return {
            "query": query,
            "retrieved_chunks": retrieved_chunks,
            "answer": response.choices[0].message.content,
            "generated_by_llm": True,
        }


if __name__ == "__main__":
    kb_dir = os.path.join(os.path.dirname(__file__), "knowledge-base")

    pipeline = RAGPipeline(kb_dir)
    stats = pipeline.build_index()
    print("Index built:", stats)

    print("\n--- Testing retrieve() (Abbas's responsibility) ---")
    query = input("Enter Your Query Here: ")
    results = pipeline.retrieve(query, top_k=3)
    print(f'Query: "{query}"')
    for r in results:
        print(f"  [{r['similarity_score']}] {r['chunk_id']} - \"{r['section_title']}\"")

    print("\n--- Testing generate_answer() (full demo, includes LLM step) ---")
    result = pipeline.generate_answer(query, top_k=2)
    print(f"Generated by LLM: {result['generated_by_llm']}")
    print(f"Answer: {result['answer']}")
    if "note" in result:
        print(f"Note: {result['note']}")
