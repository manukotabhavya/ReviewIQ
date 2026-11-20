import joblib
from utils.text_cleaner import clean_text

# Load trained model and TF-IDF vectorizer
model = joblib.load("models/sentiment_model.pkl")
tfidf = joblib.load("models/tfidf_vectorizer.pkl")


def predict_sentiment(review):

    cleaned_review = clean_text(review)

    if not cleaned_review:
        return None, 0

    review_vector = tfidf.transform([cleaned_review])

    prediction = model.predict(review_vector)[0]

    probabilities = model.predict_proba(review_vector)[0]
    confidence = max(probabilities) * 100

    return prediction, round(confidence, 2)