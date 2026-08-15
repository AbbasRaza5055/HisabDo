"""
Smart Expense Categorization - Core Engine (Day 9 POC)

Approach: TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
combined with cosine similarity. This is a classical, fully offline NLP
technique - no internet connection or model download required, unlike
transformer-based embeddings.

How it works, in plain terms:
1. We convert every known example transaction into a vector of numbers
   based on which words it contains and how distinctive those words are.
2. When a NEW transaction description comes in, we convert it the same way.
3. We compare the new vector to all known vectors using cosine similarity
   (a measure of how "similar in direction" two vectors are).
4. We assign the category of whichever known examples are most similar.

Why this approach for the POC specifically: it requires zero downloads and
zero API keys, so it can be fully built and tested end-to-end right now.
See the specification document for why a multilingual sentence-transformer
model (as proposed in Day 8) would likely perform better in production,
particularly on informal, mixed Roman Urdu/English text.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ExpenseCategorizer:
    def __init__(self, training_examples):
        """
        training_examples: list of (description, category) tuples
        """
        self.descriptions = [ex[0] for ex in training_examples]
        self.labels = [ex[1] for ex in training_examples]

        # char_wb (character n-grams within word boundaries) works better than
        # word-level n-grams for Roman Urdu text, since spelling isn't
        # standardized (e.g., "kiraya" vs "kirya") - character overlap still
        # catches these as similar even when exact words don't match.
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 4),
            lowercase=True
        )

        # Fit the vectorizer on our known examples and transform them into vectors
        self.example_vectors = self.vectorizer.fit_transform(self.descriptions)

    def categorize(self, new_description, top_k=1):
        """
        Takes a new transaction description and returns the predicted
        category along with a confidence score.
        """
        # Transform the new description using the SAME vectorizer
        # (critical - it must use the same vocabulary/weighting as training)
        new_vector = self.vectorizer.transform([new_description])

        # Compare against all known examples
        similarities = cosine_similarity(new_vector, self.example_vectors)[0]

        # Find the most similar known example(s)
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "category": self.labels[idx],
                "confidence": round(float(similarities[idx]), 4),
                "matched_example": self.descriptions[idx]
            })

        return results

    def categorize_simple(self, new_description):
        """Returns just the top predicted category and confidence, as a clean dict."""
        result = self.categorize(new_description, top_k=1)[0]
        return {
            "predicted_category": result["category"],
            "confidence": result["confidence"]
        }


if __name__ == "__main__":
    # Quick standalone test when running this file directly
    from sample_data import TRAINING_DATA, TEST_DATA

    categorizer = ExpenseCategorizer(TRAINING_DATA)

    print("=" * 60)
    print("Testing on HELD-OUT examples (not seen during setup)")
    print("=" * 60)

    correct = 0
    for description, true_category in TEST_DATA:
        prediction = categorizer.categorize_simple(description)
        is_correct = prediction["predicted_category"] == true_category
        correct += is_correct

        status = "CORRECT" if is_correct else "WRONG"
        print(f"\n[{status}] \"{description}\"")
        print(f"  True category:      {true_category}")
        print(f"  Predicted category: {prediction['predicted_category']} (confidence: {prediction['confidence']})")

    accuracy = correct / len(TEST_DATA)
    print(f"\n{'=' * 60}")
    print(f"Held-out test accuracy: {correct}/{len(TEST_DATA)} = {accuracy:.1%}")
    print("=" * 60)
