"""
Vector Database (RAG Pipeline, Stage 4)
Abbas's responsibility: Vector database

Stores chunk embeddings in a FAISS index for fast similarity search.
This uses REAL FAISS (matching Section 19's tech stack exactly) - unlike
the embeddings stage, there was no environment limitation here, so no
substitution was needed.
"""

import faiss
import numpy as np


class VectorStore:
    def __init__(self, embedding_dim):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.chunks = []  # parallel list: chunks[i] corresponds to vector i in the index

    def _normalize(self, vectors):
        """L2-normalize vectors so inner product search behaves like cosine similarity."""
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return vectors / norms

    def build(self, chunks, embeddings):
        """
        Builds the index from a list of Chunk objects and their
        corresponding embeddings (must be in the same order).
        """
        if len(chunks) != embeddings.shape[0]:
            raise ValueError(f"Mismatch: {len(chunks)} chunks but {embeddings.shape[0]} embeddings.")

        normalized = self._normalize(embeddings)
        self.index.add(normalized)
        self.chunks = list(chunks)

    def search(self, query_embedding, top_k=3):
        """
        Searches the index for the top_k chunks most similar to the query
        embedding. Returns a list of (chunk, similarity_score) tuples,
        sorted by similarity descending.
        """
        normalized_query = self._normalize(query_embedding)
        scores, indices = self.index.search(normalized_query, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.chunks[idx], float(score)))

        return results

    def save(self, index_path):
        faiss.write_index(self.index, index_path)

    @property
    def total_vectors(self):
        return self.index.ntotal


if __name__ == "__main__":
    import os
    from document_loader import load_documents
    from chunker import chunk_all_documents
    from embedder import ChunkEmbedder

    kb_dir = os.path.join(os.path.dirname(__file__), "knowledge-base")
    raw_docs = load_documents(kb_dir)
    all_chunks = chunk_all_documents(raw_docs)

    embedder = ChunkEmbedder()
    embeddings = embedder.fit_transform(all_chunks)

    store = VectorStore(embedding_dim=embeddings.shape[1])
    store.build(all_chunks, embeddings)

    print(f"Vector store built with {store.total_vectors} vectors.")

    query = "how do I export a PDF"
    query_embedding = embedder.transform(query)
    results = store.search(query_embedding, top_k=3)

    print(f"\nQuery: \"{query}\"")
    print("Top 3 results:")
    for chunk, score in results:
        print(f"  [{score:.4f}] {chunk.chunk_id} - \"{chunk.section_title}\"")
