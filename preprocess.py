
import pandas as pd
import re

# Load the original dataset
df = pd.read_csv("data/reviews.csv")

print("Original Dataset Shape:", df.shape)

# 1. Remove rows with missing review text
df = df.dropna(subset=["Review Text"])

# 2. Remove duplicate reviews
df = df.drop_duplicates(subset=["Review Text"])

# 3. Clean review text
def clean_text(text):
    text = text.lower()
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["Cleaned Review"] = df["Review Text"].apply(clean_text)

# 4. Remove empty reviews after cleaning
df = df[df["Cleaned Review"] != ""]

# 5. Create sentiment labels
def assign_sentiment(rating):
    if rating <= 2:
        return "Negative"
    elif rating == 3:
        return "Neutral"
    else:
        return "Positive"

df["Sentiment"] = df["Rating"].apply(assign_sentiment)

# 6. Save processed dataset
df.to_csv("data/processed_reviews.csv", index=False)

# Display results
print("\n========== PREPROCESSING RESULTS ==========")

print("\nProcessed Dataset Shape:", df.shape)

print("\nSentiment Distribution:")
print(df["Sentiment"].value_counts())

print("\nSample Processed Reviews:")
print(df[["Review Text", "Cleaned Review", "Rating", "Sentiment"]].head())

print("\nMissing Values in Cleaned Review:")
print(df["Cleaned Review"].isnull().sum())

print("\nProcessed dataset saved successfully!")
