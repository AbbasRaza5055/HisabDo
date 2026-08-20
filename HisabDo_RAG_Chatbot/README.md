# RAG & Knowledge Base Pipeline (HisabDo AI Copilot)

This folder contains my Day 11 submission as **RAG and Knowledge Base
Engineer** on the HisabDo AI Copilot team (architecture led by Taha,
AI/ML Team Lead). Scope: knowledge base preparation, document cleaning,
chunking, embeddings, vector database, similarity search, RAG pipeline,
and RAG evaluation — the exact 8 responsibilities assigned for this role.

## 📁 What's in this project

| File | Pipeline Stage | Description |
|---|---|---|
| `knowledge-base/` | — | 14 markdown files across faqs/, features/, guides/, blogs/ — matches Section 10 of the architecture doc exactly. |
| `document_loader.py` | 1. Cleaning | Loads .md files, strips markdown syntax while preserving content. |
| `chunker.py` | 2. Chunking | Splits documents into Q&A-unit chunks along `##` boundaries. |
| `embedder.py` | 3. Embeddings | TF-IDF vectorization (see honest note below). |
| `vector_store.py` | 4. Vector DB | Real FAISS index + cosine similarity search. |
| `rag_pipeline.py` | 5. RAG Pipeline | Wires everything together; `retrieve()` is the core deliverable. |
| `evaluate_rag.py` | 6. RAG Evaluation | 12-query labeled test set, Hit@1/Hit@3/MRR metrics. |
| `RAG_Knowledge_Base_Spec_Day11.docx` | — | Full specification, architecture alignment, and evaluation writeup. |
| `requirements.txt` | — | Exact tested dependency versions. |

## Honest Note on Technology Choice

The architecture document (Section 19) specifies **Sentence Transformers**
for embeddings. This prototype uses **TF-IDF** instead, for the same
verified reason as Day 9 and Day 10 of this capstone: the development
sandbox blocks network access to `huggingface.co` (confirmed directly
with a `PermissionDeniedError`), which is required to download Sentence
Transformer model weights.

This is a documented, deliberate substitution - not a silent downgrade.
Every other component (FAISS vector database, chunking, similarity
search, evaluation) is fully real and fully tested with no substitution.
The full reasoning, plus concrete evidence from the evaluation results
supporting the case for upgrading to Sentence Transformers in production,
is in Section 3 of the spec document.

## Evaluation Results (real, reproducible)

Run against a 12-query hand-labeled test set:

- **Hit@1: 83.3%** (10/12 queries retrieved the correct chunk as the top result)
- **Hit@3: 100%** (12/12 queries retrieved the correct chunk within the top 3)
- **Mean Reciprocal Rank: 0.903**

Verified twice - once during development, once again from a completely
clean, isolated virtual environment - with identical results both times.

## A Real Bug Caught During Development

The first version of `chunker.py` split documents into chunks *after*
`document_loader.py` had already stripped the `##` markdown markers. This
caused a short question line and its answer to be split into two
disconnected chunks instead of staying together. Caught by actually
running and inspecting the output (not assumed to work), and fixed by
chunking on the raw markdown headers first, then cleaning each resulting
chunk's text afterward. Full details in Section 4.2 of the spec document.

## Role Boundary

Per the architecture document's team structure (Section 28), this
submission's scope ends at `retrieve()` - returning ranked, relevant
chunks. The `generate_answer()` method in `rag_pipeline.py` additionally
demonstrates a full retrieval + LLM call for end-to-end demo purposes
only; the LLM/chatbot response generation itself is Omesha's
responsibility area (AI Chatbot Engineer), reused here via the same Groq
pattern from Day 10 of this capstone.

## How to Run

Install dependencies:
```bash
pip install -r requirements.txt
```

Test each pipeline stage individually:
```bash
python document_loader.py
python chunker.py
python embedder.py
python vector_store.py
```

Run the full pipeline:
```bash
python rag_pipeline.py
```

Run the evaluation:
```bash
python evaluate_rag.py
```

To test the full LLM-generation demo path, set a Groq API key first:
```bash
export GROQ_API_KEY='your-key-here'
python rag_pipeline.py
```
Without a key set, `generate_answer()` correctly falls back to returning
the top retrieved chunk directly, rather than failing or fabricating an
answer.

## Requirements
See `requirements.txt`. Key packages: numpy, scikit-learn, faiss-cpu, groq.

## Author
Abbas Raza - RAG and Knowledge Base Engineer
- GitHub: [AbbasRaza5055](https://github.com/AbbasRaza5055)

---
* Task - building and evaluating a real, working RAG pipeline against
the HisabDo AI Copilot team architecture, with full transparency about
what was tested, what was substituted, and why.*
