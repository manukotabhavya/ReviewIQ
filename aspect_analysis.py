
import re
import joblib

# Load the trained sentiment model
model = joblib.load("models/sentiment_model.pkl")
tfidf = joblib.load("models/tfidf_vectorizer.pkl")

# Define product aspects and their related keywords
aspects = {
    "Quality": ["quality", "fabric", "material", "stitching"],
    "Price": ["price", "cost", "expensive", "cheap", "worth"],
    "Delivery": ["delivery", "shipping", "arrived", "package"],
    "Comfort": ["comfortable", "comfort", "soft", "rough"],
    "Fit": ["fit", "size", "tight", "loose", "small", "large"]
}
positive_words = [
    "good", "great", "excellent", "amazing", "soft",
    "comfortable", "perfect", "beautiful", "worth",
    "satisfied", "love", "nice"
]

negative_words = [
    "bad", "poor", "terrible", "awful", "disappointed",
    "expensive", "high", "late", "rough", "uncomfortable",
    "small", "tight", "loose", "cheap", "worst"
]

negation_words = ["not", "never", "no", "isn't", "wasn't", "hardly"]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def detect_sentiment(sentence):

    words = sentence.lower().split()

    positive_count = 0
    negative_count = 0

    for i, word in enumerate(words):

        word = re.sub(r"[^a-z]", "", word)

        if word in positive_words:
            if i > 0 and words[i - 1] in negation_words:
                negative_count += 1
            else:
                positive_count += 1

        elif word in negative_words:
            if i > 0 and words[i - 1] in negation_words:
                positive_count += 1
            else:
                negative_count += 1

    if positive_count > negative_count:
        return "Positive"

    elif negative_count > positive_count:
        return "Negative"

    else:
        return "Neutral"
def analyze_aspects(review):

    sentences = re.split(
        r"[.!?]+|\bbut\b|\bhowever\b",
        review,
        flags=re.IGNORECASE
    )

    found_aspects = {}

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_lower = sentence.lower()

        for aspect, keywords in aspects.items():

            if any(keyword in sentence_lower for keyword in keywords):

                sentiment = detect_sentiment(sentence)

                found_aspects[aspect] = sentiment

    return found_aspects


print("\n========== ReviewIQ ==========")
print("Aspect-Based Sentiment Analysis")

while True:

    review = input("\nEnter a product review (or type 'exit'): ")

    if review.lower() == "exit":
        print("\nThank you for using ReviewIQ!")
        break

    results = analyze_aspects(review)

    print("\n----- ASPECT ANALYSIS -----")

    if not results:
        print("No known product aspects found.")

    else:
        for aspect, sentiment in results.items():
            print(f"{aspect}: {sentiment}")

    print("---------------------------")
