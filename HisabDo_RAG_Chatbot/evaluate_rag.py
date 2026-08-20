"""
RAG Evaluation (RAG Pipeline, Stage 6)
Abbas's responsibility: RAG evaluation

Measures retrieval quality against a labeled test set: for each test
query, we know in advance which chunk_id SHOULD be retrieved. This lets
us report real, honest metrics instead of just eyeballing a few examples.

Metrics used:
- Hit@1: was the correct chunk the TOP result?
- Hit@3: was the correct chunk somewhere in the top 3 results?
- Mean Reciprocal Rank (MRR): rewards the correct chunk appearing higher
  in the ranking, not just whether it appeared at all in the top-k.
"""

import os
from rag_pipeline import RAGPipeline

# Each entry: (query, expected_chunk_id)
EVAL_TEST_SET = [
    ("how do I export a PDF statement", "features/pdf-export.md#0"),
    ("how do I add a new customer", "features/customers.md#0"),
    ("does the app work without internet", "faqs/general.md#2"),
    ("what happens if I lose my phone", "faqs/backup.md#3"),
    ("is HisabDo free", "faqs/general.md#1"),
    ("how do I record a transaction using voice", "faqs/transactions.md#3"),
    ("how do I reset my password", "faqs/accounts.md#1"),
    ("can I edit a transaction after saving it", "faqs/transactions.md#1"),
    ("what languages does the app support", "faqs/general.md#3"),
    ("how do I delete my account", "faqs/accounts.md#3"),
    ("how do I restore my data on a new device", "faqs/backup.md#2"),
    ("what is the difference between credit given and payment received", "faqs/transactions.md#4"),
]


def evaluate_retrieval(pipeline, test_set, top_k=3):
    """
    Runs every test query through the pipeline's retrieve() method and
    checks whether the expected chunk appears in the results, at what rank.
    """
    results = []

    for query, expected_chunk_id in test_set:
        retrieved = pipeline.retrieve(query, top_k=top_k)
        retrieved_ids = [r["chunk_id"] for r in retrieved]

        if expected_chunk_id in retrieved_ids:
            rank = retrieved_ids.index(expected_chunk_id) + 1
        else:
            rank = None

        results.append({
            "query": query,
            "expected_chunk_id": expected_chunk_id,
            "retrieved_ids": retrieved_ids,
            "rank": rank,
            "hit_at_1": rank == 1,
            "hit_at_3": rank is not None and rank <= 3,
        })

    return results


def summarize_results(results):
    """Computes aggregate metrics from the per-query results."""
    n = len(results)
    hit_at_1 = sum(r["hit_at_1"] for r in results)
    hit_at_3 = sum(r["hit_at_3"] for r in results)

    reciprocal_ranks = [1 / r["rank"] if r["rank"] else 0 for r in results]
    mrr = sum(reciprocal_ranks) / n

    return {
        "total_queries": n,
        "hit_at_1_count": hit_at_1,
        "hit_at_1_rate": round(hit_at_1 / n, 3),
        "hit_at_3_count": hit_at_3,
        "hit_at_3_rate": round(hit_at_3 / n, 3),
        "mean_reciprocal_rank": round(mrr, 3),
    }


if __name__ == "__main__":
    kb_dir = os.path.join(os.path.dirname(__file__), "knowledge-base")

    pipeline = RAGPipeline(kb_dir)
    stats = pipeline.build_index()
    print("Index built:", stats)

    print(f"\nRunning evaluation on {len(EVAL_TEST_SET)} labeled test queries...\n")
    results = evaluate_retrieval(pipeline, EVAL_TEST_SET, top_k=3)

    print(f"{'Query':<55} {'Expected':<30} {'Rank':<10} {'Hit@1':<7} {'Hit@3'}")
    print("-" * 115)
    for r in results:
        rank_str = str(r["rank"]) if r["rank"] else "NOT FOUND"
        print(f"{r['query']:<55} {r['expected_chunk_id']:<30} {rank_str:<10} {str(r['hit_at_1']):<7} {r['hit_at_3']}")

    summary = summarize_results(results)
    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n--- Queries that FAILED to retrieve the expected chunk in top 3 ---")
    failures = [r for r in results if not r["hit_at_3"]]
    if failures:
        for f in failures:
            print(f"  \"{f['query']}\" -> expected {f['expected_chunk_id']}, got {f['retrieved_ids']}")
    else:
        print("  None - all queries retrieved the expected chunk within top 3.")
