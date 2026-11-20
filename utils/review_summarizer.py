
import re
import joblib
from utils.text_cleaner import clean_text

# Load trained TF-IDF vectorizer
tfidf = joblib.load("models/tfidf_vectorizer.pkl")


def summarize_reviews(reviews, top_n=3):

    sentences = []

    # Split reviews into individual sentences
    for review in reviews:

        parts = re.split(r"[.!?]+", str(review))

        for sentence in parts:

            sentence = sentence.strip()

            if sentence:
                sentences.append(sentence)

    if not sentences:
        return []

    # Clean sentences
    cleaned_sentences = [
        clean_text(sentence) for sentence in sentences
    ]

    # Convert sentences into TF-IDF vectors
    vectors = tfidf.transform(cleaned_sentences)

    # Calculate importance scores
    scores = vectors.sum(axis=1).A1

    # Rank sentences by importance
    ranked_sentences = sorted(
        zip(range(len(sentences)), sentences, scores),
        key=lambda x: x[2],
        reverse=True
    )

    # Select top sentences
    selected_indices = sorted(
        [item[0] for item in ranked_sentences[:top_n]]
    )

    return [sentences[i] for i in selected_indices]
