"""
Day 9 - Smart Expense Categorization API (POC)
Remote Internship Task

Exposes the TF-IDF categorization engine through a POST /categorize endpoint,
following the same FastAPI pattern used in Day 7.

Run with:
    uvicorn main:app --reload

Then visit http://127.0.0.1:8000/docs to test interactively.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from categorizer import ExpenseCategorizer
from sample_data import TRAINING_DATA, CATEGORIES

app = FastAPI(
    title="Smart Expense Categorization API (POC)",
    description="Suggests a category for a transaction description using TF-IDF + cosine similarity.",
    version="1.0.0"
)

# Build the categorizer once at startup (not per-request, for speed)
categorizer = ExpenseCategorizer(TRAINING_DATA)

# A confidence threshold below which we tell the app to treat the
# suggestion as "low confidence" rather than auto-applying it silently.
# This threshold was chosen based on testing ambiguous inputs during
# development (see README) - vague descriptions consistently scored below
# this line, while clear ones scored well above it.
LOW_CONFIDENCE_THRESHOLD = 0.30


class TransactionInput(BaseModel):
    description: str = Field(
        ..., min_length=1, max_length=300,
        description="The transaction description, as entered by the user (any supported language/mix).",
        examples=["kirana samaan wholesale market se khareeda"]
    )


class CategorizationOutput(BaseModel):
    predicted_category: str
    confidence: float
    is_low_confidence: bool
    available_categories: list[str]


@app.get("/")
def read_root():
    return {
        "message": "Smart Expense Categorization API is running.",
        "docs": "Visit /docs for interactive API documentation.",
        "endpoint": "POST /categorize",
        "available_categories": CATEGORIES
    }


@app.post("/categorize", response_model=CategorizationOutput)
def categorize_transaction(transaction: TransactionInput):
    """
    Takes a transaction description and suggests the most likely category,
    along with a confidence score.
    """
    try:
        result = categorizer.categorize_simple(transaction.description)

        return CategorizationOutput(
            predicted_category=result["predicted_category"],
            confidence=result["confidence"],
            is_low_confidence=result["confidence"] < LOW_CONFIDENCE_THRESHOLD,
            available_categories=CATEGORIES
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Categorization failed: {str(e)}")
