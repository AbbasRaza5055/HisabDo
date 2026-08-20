"""
Embeddings (RAG Pipeline, Stage 3)
Abbas's responsibility: Embeddings

Converts each text chunk into a numerical vector representation, so
chunks can be compared for similarity in the next stage.

HONEST NOTE ON TECHNOLOGY CHOICE:
Section 19 of the HisabDo AI Copilot architecture document specifies
Sentence Transformers (multilingual) as the recommended embedding model.
This POC uses TF-IDF vectorization instead, for the same reason
documented in the Day 9 capstone submission: the development sandbox
used to build this POC blocks network access to huggingface.co (confirmed
directly - a real PermissionDeniedError/403, not a guess), which is
required to download Sentence Transformer model weights.

TF-IDF is a real, legitimate embedding technique - not a placeholder -
and everything built on top of it in this POC (vector database, similarity
search, RAG pipeline) is fully real and fully tested. However, Sentence
Transformers remains the correct production recommendation, since it
would likely understand semantic similarity (not just word/character
overlap) much better - especially important for a multilingual knowledge
base where a question phrased differently from the document text should
still retrieve the right chunk.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class ChunkEmbedder:
    def __init__(self):
        # char_wb (character n-grams within word boundaries) - same choice
        # as Day 9's categorizer, for the same reason: it handles informal,
        # non-standardized Roman Urdu spelling better than word-level matching.
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 4),
            lowercase=True,
        )
        self.is_fitted = False

    def fit_transform(self, chunks):
        """
        Fits the vectorizer on a list of Chunk objects and returns their
        embeddings as a numpy array (shape: [num_chunks, vocab_size]).
        This is called once, when building the knowledge base index.
        """
        texts = [chunk.text for chunk in chunks]
        embeddings = self.vectorizer.fit_transform(texts)
        self.is_fitted = True
        return embeddings.toarray().astype("float32")

    def transform(self, text):
        """
        Embeds a single new piece of text (e.g., a user's question) using
        the ALREADY-FITTED vectorizer - critical that this uses the same
        vocabulary/weighting learned during fit_transform, not a new fit.
        """
        if not self.is_fitted:
            raise RuntimeError("Vectorizer must be fitted with fit_transform() before calling transform().")
        embedding = self.vectorizer.transform([text])
        return embedding.toarray().astype("float32")


if __name__ == "__main__":
    import os
    from document_loader import load_documents
    from chunker import chunk_all_documents

    kb_dir = os.path.join(os.path.dirname(__file__), "knowledge-base")
    raw_docs = load_documents(kb_dir)
    all_chunks = chunk_all_documents(raw_docs)

    embedder = ChunkEmbedder()
    embeddings = embedder.fit_transform(all_chunks)

    print(f"Embedded {len(all_chunks)} chunks.")
    print(f"Embedding matrix shape: {embeddings.shape}")
    print(f"Vocabulary size (embedding dimension): {len(embedder.vectorizer.vocabulary_)}")

    query_embedding = embedder.transform("how do I export a statement")
    print(f"\nQuery embedding shape: {query_embedding.shape}")
    print(f"Matches chunk embedding dimension: {query_embedding.shape[1] == embeddings.shape[1]}")
