
import re
from utils.text_cleaner import clean_text

# Product aspects and related keywords
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


def detect_sentiment(sentence):

    words = sentence.lower().split()

    positive_count = 0
    negative_count = 0

    for i, word in enumerate(words):

        word = re.sub(r"[^a-z]", "", word)

        previous_word = ""

        if i > 0:
            previous_word = re.sub(r"[^a-z]", "", words[i - 1])

        if word in positive_words:

            if previous_word in negation_words:
                negative_count += 1
            else:
                positive_count += 1

        elif word in negative_words:

            if previous_word in negation_words:
                positive_count += 1
            else:
                negative_count += 1

    if positive_count > negative_count:
        return "Positive"

    elif negative_count > positive_count:
        return "Negative"

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
