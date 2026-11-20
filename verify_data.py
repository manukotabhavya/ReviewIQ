
import pandas as pd

# Load processed dataset
df = pd.read_csv("data/processed_reviews.csv")

print("\n========== PROCESSED DATA VERIFICATION ==========")

print("\nDataset Shape:", df.shape)

print("\nSentiment Distribution:")
print(df["Sentiment"].value_counts())

print("\nSentiment Percentages:")
print(df["Sentiment"].value_counts(normalize=True) * 100)

print("\nSample Cleaned Reviews:")
for review in df["Cleaned Review"].head(5):
    print("-", review)

print("\nMissing Cleaned Reviews:", df["Cleaned Review"].isnull().sum())

print("\nDuplicate Cleaned Reviews:", df["Cleaned Review"].duplicated().sum())

print("\n========== VERIFICATION COMPLETED ==========")
