import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

# Load processed dataset
df = pd.read_csv("data/processed_reviews.csv")
df = df.drop_duplicates(subset=["Cleaned Review"])

X = df["Cleaned Review"]
y = df["Sentiment"]

# Split dataset (same settings used during training)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Load trained model and TF-IDF vectorizer
model = joblib.load("models/sentiment_model.pkl")
tfidf = joblib.load("models/tfidf_vectorizer.pkl")

# Transform test reviews
X_test_tfidf = tfidf.transform(X_test)

# Make predictions
y_pred = model.predict(X_test_tfidf)

# Evaluation
print("\n========== ReviewIQ Model Evaluation ==========")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(
    y_test,
    y_pred,
    labels=["Negative", "Neutral", "Positive"]
))
# Confusion Matrix Visualization
cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["Negative", "Neutral", "Positive"]
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Negative", "Neutral", "Positive"],
    yticklabels=["Negative", "Neutral", "Positive"]
)

plt.title("ReviewIQ - Sentiment Confusion Matrix")
plt.xlabel("Predicted Sentiment")
plt.ylabel("Actual Sentiment")

plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=300, bbox_inches="tight")
plt.show()