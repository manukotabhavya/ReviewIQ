import joblib
from utils.text_cleaner import clean_text

# Load trained TF-IDF vectorizer
tfidf = joblib.load("models/tfidf_vectorizer.pkl")


def extract_keywords(review, top_n=5):

    cleaned_review = clean_text(review)

    if not cleaned_review:
        return []

    vector = tfidf.transform([cleaned_review])

    feature_names = tfidf.get_feature_names_out()
    scores = vector.toarray()[0]

    keywords = sorted(
        zip(feature_names, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        word for word, score in keywords if score > 0
    ][:top_n]