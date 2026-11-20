
import re
import joblib

# Load the trained TF-IDF vectorizer
tfidf = joblib.load("models/tfidf_vectorizer.pkl")


def summarize_reviews(reviews, top_n=3):

    sentences = []

    # Split reviews into sentences
    for review in reviews:
        parts = re.split(r"[.!?]+", str(review))

        for sentence in parts:
            sentence = sentence.strip()

            if sentence:
                sentences.append(sentence)

    if not sentences:
        return []

    # Convert sentences into TF-IDF vectors
    vectors = tfidf.transform(sentences)

    # Calculate importance score for each sentence
    scores = vectors.sum(axis=1).A1

    # Select the most important sentences
    ranked_sentences = sorted(
        zip(sentences, scores),
        key=lambda x: x[1],
        reverse=True
    )

    # Return top sentences in their original order
    selected = ranked_sentences[:top_n]

    selected_sentences = [
        sentence for sentence, score in selected
    ]

    return selected_sentences


print("\n========== ReviewIQ ==========")
print("Customer Review Summarization")

print("\nEnter customer reviews.")
print("Type 'done' when finished.")

reviews = []

while True:

    review = input("\nEnter review: ")

    if review.lower() == "done":
        break

    if review.strip():
        reviews.append(review)

if reviews:

    summary = summarize_reviews(reviews)

    print("\n----- REVIEW SUMMARY -----")

    for sentence in summary:
        print("-", sentence)

    print("--------------------------")

else:
    print("No reviews entered.")
