"""
Retrieval stage of the RAG pipeline.

Instead of exact keyword matching, this uses TF-IDF: it looks at ALL the
words in a section's text and weighs how important each word is (common
words like "the" matter less, rare/specific words like "eviction" or
"cognizable" matter more). Then it compares the user's query against every
section using that weighting and returns the closest matches - even if the
wording isn't identical.

This is a well-understood, classical technique (no internet/API needed),
and a reasonable stand-in until you plug in real neural embeddings later.
"""

import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Default path works no matter which folder you run the script from
_DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "sections.json"
)


class LawRetriever:
    def __init__(self, data_path=_DEFAULT_DATA_PATH):
        with open(data_path, "r", encoding="utf-8") as f:
            self.sections = json.load(f)

        # Build one searchable text blob per section: title + summary + keywords.
        # The more relevant text you put in here, the better retrieval gets.
        self.documents = [
            f"{s['title']}. {s['summary']} {' '.join(s.get('keywords', []))}"
            for s in self.sections
        ]

        # Learn word importance weights across all sections, then convert
        # every section's text into a numeric vector.
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.doc_vectors = self.vectorizer.fit_transform(self.documents)

    def retrieve(self, query, top_k=3, min_score=0.05):
        """
        Returns the top_k most relevant sections for a query, each with
        a similarity score (0 to 1). Sections below min_score are dropped -
        this is what lets the system say "no good match" instead of
        forcing a weak/irrelevant result.
        """
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.doc_vectors)[0]

        # Pair each section with its score, sort by score descending
        ranked = sorted(
            zip(self.sections, scores), key=lambda pair: pair[1], reverse=True
        )

        results = [
            (section, float(score))
            for section, score in ranked[:top_k]
            if score >= min_score
        ]
        return results


if __name__ == "__main__":
    # Quick manual test
    retriever = LawRetriever()
    test_query = "my neighbour keeps threatening to hurt me"
    results = retriever.retrieve(test_query)

    print(f"Query: {test_query}\n")
    for section, score in results:
        print(f"[{score:.2f}] {section['act']} Sec {section['section']} - {section['title']}")