# Day 9 - Smart Expense Categorization: Spec + Working POC (Remote Internship Task)

This folder contains my Day 9 capstone submission — a detailed specification
and a fully working, fully tested proof-of-concept for the Smart Expense/
Transaction Categorization AI feature (selected from Day 8's 5 use cases).

## 📁 What's in this project

| File | Description |
|---|---|
| `Smart_Expense_Categorization_Spec_Day9.docx` | Full specification: workflow, model research, integration plan, POC results, architecture diagram. |
| `categorizer.py` | Core categorization engine (TF-IDF + cosine similarity). |
| `sample_data.py` | 38 training examples + 8 held-out test examples (Roman Urdu + English). |
| `main.py` | FastAPI app exposing `POST /categorize`. |
| `requirements.txt` | Exact tested dependency versions. |

## 🧠 Honest Note on Technology Choice

The spec document (Section 3.1) explains this directly, but to be upfront
here too: the original plan was to use a multilingual sentence-transformer
model (as proposed in Day 8), matching the pattern already used successfully
in an earlier internship project (Customer Support Agent). During development,
the build environment returned a **403 Forbidden** from `huggingface.co`,
meaning the model weights could not be downloaded there.

Rather than submit untested code built against a library that couldn't
actually run, this POC uses **TF-IDF + cosine similarity** (via scikit-learn)
instead — a real, legitimate, fully offline NLP technique with zero download
dependency. Every result in the spec document was actually run and verified,
including honest test cases on genuinely ambiguous input where the system's
confidence score correctly drops. The spec document explains why the
multilingual sentence-transformer approach remains the recommended path for
a production deployment.

## 📊 Test Results Summary

- **8/8 (100%)** correct on held-out test examples not seen during setup.
- Confidence scores meaningfully drop on genuinely ambiguous input (e.g.,
  "paisay diye" — "gave money," with no real category signal — scored
  0.218 and was correctly flagged as low-confidence).
- This directly validates the product design decision to show AI category
  suggestions as **editable/confirmable**, not silently auto-applied.

## ▶️ How to Run the POC

Install dependencies:
```bash
pip install -r requirements.txt
```

Test the categorization engine directly (no server needed):
```bash
python categorizer.py
```

Run the API:
```bash
uvicorn main:app --reload
```
Visit `http://127.0.0.1:8000/docs` to test interactively, or:
```bash
curl -X POST http://127.0.0.1:8000/categorize \
  -H "Content-Type: application/json" \
  -d '{"description": "kirana samaan wholesale market se khareeda"}'
```

## 🛠️ Requirements
See `requirements.txt`. Key packages: fastapi, uvicorn, pydantic, scikit-learn, numpy.

## 👤 Author
Abbas Raza
- GitHub: [AbbasRaza5055](https://github.com/AbbasRaza5055)

---
*Day 9 task — moving from AI ideas (Day 8) to a concrete, working proof-of-concept,
including honest testing of both clear and ambiguous real-world input.*
