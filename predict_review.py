
import re
import joblib

# Load saved model and vectorizer
model = joblib.load("models/sentiment_model.pkl")
tfidf = joblib.load("models/tfidf_vectorizer.pkl")

# Clean user review
def clean_text(text):
    text = text.lower()
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

print("\n========== ReviewIQ ==========")
print("AI Product Review Intelligence")

while True:

    review = input("\nEnter a product review (or type 'exit'): ")

    if review.lower() == "exit":
        print("\nThank you for using ReviewIQ!")
        break

    cleaned_review = clean_text(review)

    if not cleaned_review:
        print("Please enter a valid review.")
        continue

    # Convert review into TF-IDF features
    review_vector = tfidf.transform([cleaned_review])

    # Predict sentiment
    prediction = model.predict(review_vector)[0]

    # Calculate confidence
    probabilities = model.predict_proba(review_vector)[0]
    confidence = max(probabilities) * 100

    print("\n----- ANALYSIS RESULT -----")
    print("Review:", review)
    print("Predicted Sentiment:", prediction)
    print("Confidence:", round(confidence, 2), "%")
    print("---------------------------")
