# 💜 ReviewIQ – AI Product Review Intelligence

**Less scrolling through reviews, more understanding what customers really think!**

ReviewIQ is an AI-powered product review analysis application built using Python, Machine Learning, and Natural Language Processing (NLP). It transforms customer reviews into meaningful insights through sentiment analysis, aspect analysis, keyword extraction, and review summarization.

## 🚀 Live Demo

[Launch ReviewIQ](https://reviewiq-oyrkumkjic2mm3spf9iqcp.streamlit.app/)

## ✨ Features

### 1. Sentiment Analysis
- Classifies customer reviews into Positive, Negative, and Neutral categories.
- Uses a trained Machine Learning model.
- Displays prediction confidence.

### 2. Aspect-Based Sentiment Analysis
Analyzes customer opinions about different product aspects:
- Quality
- Price
- Delivery
- Comfort
- Fit

### 3. Important Keyword Extraction
- Extracts important keywords from customer reviews.
- Uses TF-IDF-based keyword extraction.

### 4. Review Summarization
- Extracts important sentences from multiple customer reviews.
- Helps users understand the main feedback quickly.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Machine Learning:** Scikit-learn
- **NLP:** TF-IDF, Text Preprocessing
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Web Application:** Streamlit
- **Model Persistence:** Joblib

## 📂 Project Structure

```text
ReviewIQ/
│
├── app.py
├── data/
│   ├── reviews.csv
│   ├── processed_reviews.csv
│   └── model_comparison.csv
│
├── models/
│   ├── sentiment_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── utils/
│   ├── __init__.py
│   ├── text_cleaner.py
│   ├── sentiment_analyzer.py
│   ├── aspect_analyzer.py
│   ├── keyword_extractor.py
│   └── review_summarizer.py
│
├── explore_data.py
├── preprocess.py
├── train_model.py
├── compare_models.py
├── evaluate_model.py
├── predict_review.py
├── aspect_analysis.py
├── keyword_extraction.py
├── review_summary.py
├── verify_data.py
├── confusion_matrix.png
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/manukotabhavya/ReviewIQ.git
```

### 2. Navigate to the project directory

```bash
cd ReviewIQ
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 🧠 Machine Learning Approach

- Text preprocessing and cleaning
- TF-IDF vectorization
- Logistic Regression for sentiment classification
- Keyword-based aspect sentiment analysis
- TF-IDF-based keyword extraction
- Extractive review summarization

## 📊 Dataset

The project uses the Women's E-Commerce Clothing Reviews dataset containing customer reviews and product-related information.

## 🎯 Project Objective

The main objective of ReviewIQ is to simplify customer feedback analysis and help users understand customer opinions without manually reading large numbers of reviews.

## 👩‍💻 Developed By

**Bhavya Sri Sai Manukota**

B.Tech – Computer Science and Engineering (AI & ML)

[GitHub](https://github.com/manukotabhavya)

---

⭐ If you find this project interesting, consider giving the repository a star!