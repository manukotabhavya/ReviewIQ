
import re
import joblib

# Load the trained TF-IDF vectorizer
tfidf = joblib.load("models/tfidf_vectorizer.pkl")


def extract_keywords(review, top_n=5):

    # Clean the review
    review = review.lower()
    review = re.sub(r"[^a-zA-Z\s]", " ", review)
    review = re.sub(r"\s+", " ", review).strip()

    if not review:
        return []

    # Convert review into TF-IDF features
    vector = tfidf.transform([review])

    # Get feature names and their TF-IDF scores
    feature_names = tfidf.get_feature_names_out()
    scores = vector.toarray()[0]

    # Sort keywords by importance
    keywords = sorted(
        zip(feature_names, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # Return top keywords with non-zero scores
    return [
        word for word, score in keywords
        if score > 0
    ][:top_n]


print("\n========== ReviewIQ ==========")
print("Customer Review Keyword Extraction")

while True:

    review = input("\nEnter a product review (or type 'exit'): ")

    if review.lower() == "exit":
        print("\nThank you for using ReviewIQ!")
        break

    keywords = extract_keywords(review)

    print("\n----- IMPORTANT KEYWORDS -----")

    if keywords:
        for keyword in keywords:
            print("-", keyword)
    else:
        print("No important keywords found.")

    print("------------------------------")
