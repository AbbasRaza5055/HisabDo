"""
Document Loading & Cleaning (RAG Pipeline, Stage 1)
Abbas's responsibility: Knowledge base preparation, Document cleaning

Loads every .md file from the knowledge-base/ folder and cleans it up
before chunking: stripping markdown syntax that would add noise to
embeddings (headers, bold/italic markers, extra whitespace) while
preserving the actual readable text.
"""

import os
import re
from dataclasses import dataclass


@dataclass
class RawDocument:
    """A single loaded document with its source metadata, before cleaning."""
    filepath: str
    category: str  # the parent folder name: faqs, features, guides, blogs
    filename: str
    raw_text: str


@dataclass
class CleanedDocument:
    """A document after cleaning, ready for chunking."""
    filepath: str
    category: str
    filename: str
    cleaned_text: str


def load_documents(knowledge_base_dir):
    """
    Walks the knowledge-base directory and loads every .md file,
    recording which category folder (faqs/features/guides/blogs) it
    came from - this metadata travels with the document all the way
    through to the final retrieval result, so we can show the user
    where an answer came from.
    """
    documents = []

    for category in sorted(os.listdir(knowledge_base_dir)):
        category_path = os.path.join(knowledge_base_dir, category)
        if not os.path.isdir(category_path):
            continue

        for filename in sorted(os.listdir(category_path)):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(category_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()

            documents.append(RawDocument(
                filepath=filepath,
                category=category,
                filename=filename,
                raw_text=raw_text,
            ))

    return documents


def clean_text(raw_text):
    """
    Cleans a single document's raw markdown text:
    - Removes markdown header symbols (#, ##, ###) but keeps the header text
    - Removes bold/italic markers (**text**, *text*)
    - Collapses multiple blank lines into one
    - Strips leading/trailing whitespace

    We keep the actual words (they carry meaning for embeddings/TF-IDF),
    we only strip the markdown SYNTAX around them, since symbols like
    "#" or "**" don't carry semantic meaning and would just be noise.
    """
    text = raw_text

    # Remove markdown header symbols, keep the header text itself
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

    # Remove bold/italic markers
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)

    # Collapse 3+ newlines down to 2 (paragraph break)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip trailing whitespace on each line
    text = "\n".join(line.rstrip() for line in text.split("\n"))

    return text.strip()


def clean_documents(raw_documents):
    """Applies clean_text to a list of RawDocuments, returning CleanedDocuments."""
    cleaned = []
    for doc in raw_documents:
        cleaned.append(CleanedDocument(
            filepath=doc.filepath,
            category=doc.category,
            filename=doc.filename,
            cleaned_text=clean_text(doc.raw_text),
        ))
    return cleaned


if __name__ == "__main__":
    kb_dir = os.path.join(os.path.dirname(__file__), "knowledge-base")
    raw_docs = load_documents(kb_dir)
    print(f"Loaded {len(raw_docs)} documents:")
    for doc in raw_docs:
        print(f"  [{doc.category}] {doc.filename} ({len(doc.raw_text)} chars)")

    cleaned_docs = clean_documents(raw_docs)
    print(f"\nCleaned {len(cleaned_docs)} documents.")
    print("\n--- Example: before/after cleaning (first 300 chars of general.md) ---")
    general_raw = next(d for d in raw_docs if d.filename == "general.md")
    general_clean = next(d for d in cleaned_docs if d.filename == "general.md")
    print("BEFORE:\n", general_raw.raw_text[:300])
    print("\nAFTER:\n", general_clean.cleaned_text[:300])
