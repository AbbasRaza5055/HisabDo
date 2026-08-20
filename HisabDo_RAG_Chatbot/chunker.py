"""
Text Chunking (RAG Pipeline, Stage 2)
Abbas's responsibility: Chunking

Splits each document into smaller "chunks" - the actual units that get
embedded and retrieved. Chunk size matters a lot for RAG quality: too
large and irrelevant details get mixed into a retrieved chunk; too small
and you lose context.
"""

import re
from dataclasses import dataclass
from document_loader import load_documents, clean_text


@dataclass
class Chunk:
    """A single retrievable chunk of text, with metadata tracing it back to its source document."""
    chunk_id: str
    text: str
    source_category: str
    source_filename: str
    section_title: str


def chunk_document(raw_doc, min_chunk_chars=30):
    """
    Splits a RAW (uncleaned) document's markdown text into chunks along
    '## ' section headers, so each chunk is exactly one complete
    question+answer (or topic+explanation) unit. Cleaning is applied
    AFTER splitting, to each chunk's text individually.
    """
    # Split on lines starting with "## " (level-2 headers), keeping the
    # header text with the section that follows it
    raw_sections = re.split(r"(?m)^##\s+", raw_doc.raw_text)

    chunks = []
    chunk_index = 0

    # The first element before any "## " is the document's H1 title/intro -
    # skip it as a standalone chunk, it's not a retrievable Q&A unit
    for section in raw_sections[1:]:
        section = section.strip()
        if not section:
            continue

        lines = section.split("\n", 1)
        section_title = clean_text(lines[0].strip())
        section_body = lines[1].strip() if len(lines) > 1 else ""

        full_text = clean_text(section)

        if len(full_text) < min_chunk_chars:
            continue

        chunk_id = f"{raw_doc.category}/{raw_doc.filename}#{chunk_index}"
        chunks.append(Chunk(
            chunk_id=chunk_id,
            text=full_text,
            source_category=raw_doc.category,
            source_filename=raw_doc.filename,
            section_title=section_title,
        ))
        chunk_index += 1

    return chunks


def chunk_all_documents(raw_documents):
    """Chunks every document in a list, returning one flat list of all chunks."""
    all_chunks = []
    for doc in raw_documents:
        all_chunks.extend(chunk_document(doc))
    return all_chunks


if __name__ == "__main__":
    import os
    kb_dir = os.path.join(os.path.dirname(__file__), "knowledge-base")

    raw_docs = load_documents(kb_dir)
    all_chunks = chunk_all_documents(raw_docs)

    print(f"Created {len(all_chunks)} chunks from {len(raw_docs)} documents.")
    print(f"Average chunks per document: {len(all_chunks) / len(raw_docs):.1f}")

    print("\n--- Example chunks from pdf-export.md (verifying the fix) ---")
    pdf_chunks = [c for c in all_chunks if c.source_filename == "pdf-export.md"]
    for c in pdf_chunks:
        print(f"\n[{c.chunk_id}]")
        print(f"Section title: {c.section_title}")
        print(f"Full text: {c.text}")
