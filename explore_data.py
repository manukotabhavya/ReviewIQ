
import pandas as pd

# Load the dataset
df = pd.read_csv("data/reviews.csv")

# Display dataset information
print("\n========== DATASET OVERVIEW ==========")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nRating Distribution:")
print(df["Rating"].value_counts().sort_index())

print("\nRecommendation Distribution:")
print(df["Recommended IND"].value_counts())

print("\nSample Customer Reviews:")
for review in df["Review Text"].dropna().head(5):
    print("\n", review)

print("\n========== EXPLORATION COMPLETED ==========")
