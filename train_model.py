
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load processed dataset
df = pd.read_csv("data/processed_reviews.csv")

# Remove duplicate cleaned reviews
df = df.drop_duplicates(subset=["Cleaned Review"])

# Select features and target
X = df["Cleaned Review"]
y = df["Sentiment"]

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# Convert text into numerical features
tfidf = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    min_df=2,
    stop_words="english"
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

print("\nTF-IDF Transformation Completed!")
print("Training Matrix Shape:", X_train_tfidf.shape)

# Train Logistic Regression model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_tfidf, y_train)

print("\nModel Training Completed!")

# Make predictions
y_pred = model.predict(X_test_tfidf)

# Evaluate model
print("\n========== MODEL EVALUATION ==========")

print("\nAccuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=["Negative", "Neutral", "Positive"]))

# Save trained model and vectorizer
joblib.dump(model, "models/sentiment_model.pkl")
joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")

print("\nModel and TF-IDF Vectorizer Saved Successfully!")
