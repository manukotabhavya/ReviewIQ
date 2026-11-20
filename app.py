
import streamlit as st
import streamlit.components.v1 as components
import html
import textwrap

from utils.sentiment_analyzer import predict_sentiment
from utils.aspect_analyzer import analyze_aspects
from utils.keyword_extractor import extract_keywords
from utils.review_summarizer import summarize_reviews


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ReviewIQ | AI Fashion Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "active_slide" not in st.session_state:
    st.session_state.active_slide = "01 Sentiment"

if "summary_results" not in st.session_state:
    st.session_state.summary_results = None


# =========================================================
# MAIN APPLICATION CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --background: #F8F6FC;
    --white: #FFFFFF;
    --black: #17121F;
    --lavender: #F0EAF9;
    --purple: #DCD0F4;
    --purple-dark: #9275C6;
    --border: #EAE4F2;
}

.stApp {
    background: var(--background);
    color: var(--black);
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

/* TEXT */

.stApp p,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp span {
    color: var(--black);
}

/* BRAND */

.brand {
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #17121F;
}

.brand span {
    font-family: 'Playfair Display', serif;
}

.nav-label {
    text-align: right;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    padding-top: 13px;
}

/* HEADINGS */

.section-kicker {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2.5px;
    color: #9275C6 !important;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 31px;
    color: #17121F;
    margin: 7px 0;
}

.section-description {
    font-size: 13px;
    line-height: 1.7;
    color: #62596D !important;
    margin-bottom: 20px;
}

/* INPUTS */

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] * {
    color: #17121F !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}

.stTextArea textarea {
    background: #FFFFFF !important;
    color: #17121F !important;
    -webkit-text-fill-color: #17121F !important;
    caret-color: #17121F !important;
    border: 1px solid #E2D9EF !important;
    border-radius: 15px !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
    padding: 16px !important;
}

.stTextArea textarea::placeholder {
    color: #17121F !important;
    -webkit-text-fill-color: #17121F !important;
    opacity: 0.60 !important;
}

.stTextArea textarea:focus {
    border: 1px solid #9275C6 !important;
    box-shadow: 0 0 0 2px #E8DDF8 !important;
}

/* FLOATING CONTAINERS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid #EEE8F5 !important;
    border-radius: 20px !important;
    box-shadow: 0 6px 22px rgba(48, 34, 70, 0.055);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 13px 30px rgba(48, 34, 70, 0.10);
}

/* BUTTONS */

.stButton > button {
    background: #DCD0F4 !important;
    color: #17121F !important;
    border: 1px solid #D3C4EB !important;
    border-radius: 14px !important;
    min-height: 48px;
    font-weight: 800 !important;
    box-shadow: 0 6px 16px rgba(92, 65, 135, 0.12);
    transition: all 0.25s ease !important;
}

.stButton > button * {
    color: #17121F !important;
}

.stButton > button:hover {
    background: #CDBCEB !important;
    border-color: #BCA7DF !important;
    transform: translateY(-3px);
    box-shadow: 0 10px 22px rgba(92, 65, 135, 0.19);
}

/* NAVIGATION */

div[role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

div[role="radiogroup"] label {
    background: #FFFFFF !important;
    border: 1px solid #EAE4F2 !important;
    border-radius: 14px !important;
    padding: 12px 18px !important;
    box-shadow: 0 4px 13px rgba(48, 34, 70, 0.05);
    transition: all 0.2s ease;
}

div[role="radiogroup"] label:hover {
    background: #F0EAF9 !important;
    transform: translateY(-2px);
}

/* METRICS */

.metric-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 37px;
    margin: 14px 0 7px;
}

.metric-description {
    font-size: 12px;
    color: #62596D !important;
}

/* ASPECT CARDS */

.aspect-card {
    background: #FFFFFF;
    border: 1px solid #EEE8F5;
    border-radius: 17px;
    padding: 23px;
    margin-bottom: 13px;
    box-shadow: 0 5px 18px rgba(48, 34, 70, 0.055);
    transition: all 0.25s ease;
}

.aspect-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 13px 28px rgba(48, 34, 70, 0.11);
}

.aspect-name {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.aspect-value {
    font-size: 19px;
    font-weight: 800;
    margin-top: 13px;
}

/* KEYWORDS */

.keyword-chip {
    display: inline-block;
    background: #F0EAF9;
    border: 1px solid #E2D8F1;
    border-radius: 30px;
    padding: 12px 19px;
    margin: 6px;
    font-size: 13px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.keyword-chip:hover {
    background: #DCD0F4;
    transform: translateY(-3px);
}

/* EMPTY STATES */

.empty-state {
    background: #FFFFFF !important;
    color: #17121F !important;
    border: 1px solid #EAE4F2 !important;
    border-radius: 17px;
    padding: 22px 25px;
    margin: 12px 0;
    font-size: 14px;
    font-weight: 600;
    box-shadow: 0 6px 20px rgba(48, 34, 70, 0.06);
}

/* PURPLE SUCCESS MESSAGE */

.success-message {
    background: #E8DDF8;
    color: #493267;
    border: 1px solid #D4C3ED;
    border-radius: 15px;
    padding: 14px 20px;
    margin: 14px 0;
    font-size: 14px;
    font-weight: 700;
    box-shadow: 0 5px 16px rgba(92, 65, 135, 0.09);
}

/* SUMMARY */

.summary-item {
    background: #F8F6FC;
    border: 1px solid #EEE8F5;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 12px;
    font-size: 14px;
    line-height: 1.8;
}

/* ALERTS */

[data-testid="stAlert"] {
    background: #F0EAF9 !important;
    border: 1px solid #E2D8F1 !important;
    border-radius: 15px !important;
}

[data-testid="stAlert"] * {
    color: #17121F !important;
}

/* PROGRESS */

.stProgress > div > div {
    background: #9275C6 !important;
}

.stProgress > div {
    background: #EEE8F5 !important;
}

/* REMOVE DIVIDERS */

hr {
    display: none !important;
}

/* FOOTER */

.footer {
    text-align: center;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 35px 0 10px;
    color: #62596D;
}

/* MOBILE */

@media (max-width: 750px) {
    .section-title {
        font-size: 25px;
    }

    div[role="radiogroup"] {
        gap: 6px;
    }

    div[role="radiogroup"] label {
        padding: 9px 10px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO HTML COMPONENT
# =========================================================

hero_component = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: 'DM Sans', sans-serif;
}

.hero {
    position: relative;
    width: 100%;
    height: 335px;
    overflow: hidden;
    border-radius: 25px;
    padding: 48px 42px;
    background: linear-gradient(
        120deg,
        #F0EAF9,
        #E8DFF5 55%,
        #E4D9F2
    );
    box-shadow: 0 10px 30px rgba(75, 48, 110, 0.08);
}

.hero-content {
    position: relative;
    z-index: 5;
    max-width: 590px;
}

.hero-kicker {
    color: #70568F;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
}

.hero-title {
    color: #17121F;
    font-family: Georgia, serif;
    font-size: clamp(34px, 4.5vw, 55px);
    line-height: 1.18;
    margin: 18px 0;
    letter-spacing: -1.5px;
}

.hero-title span {
    color: #8061AE;
    font-style: italic;
}

.hero-description {
    color: #51465F;
    font-size: 14px;
    line-height: 1.9;
    max-width: 480px;
}

.fashion-decoration {
    position: absolute;
    inset: 0;
    pointer-events: none;
}

.floating-item {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 76px;
    height: 76px;
    border-radius: 23px;
    background: rgba(255, 255, 255, 0.78);
    border: 1px solid rgba(255, 255, 255, 0.95);
    box-shadow: 0 12px 28px rgba(75, 48, 110, 0.13);
    font-size: 38px;
    animation: floatAround 6s ease-in-out infinite;
    backdrop-filter: blur(8px);
}

.item-one {
    top: 13%;
    right: 27%;
    animation-delay: 0s;
}

.item-two {
    top: 53%;
    right: 8%;
    animation-delay: -1.5s;
    animation-duration: 7s;
}

.item-three {
    top: 10%;
    right: 6%;
    animation-delay: -3s;
    animation-duration: 8s;
}

.item-four {
    top: 65%;
    right: 35%;
    animation-delay: -2s;
    animation-duration: 6.5s;
}

.item-five {
    top: 36%;
    right: 17%;
    animation-delay: -4s;
    animation-duration: 7.5s;
}

@keyframes floatAround {
    0% {
        transform: translate(0, 0) rotate(-8deg);
    }

    25% {
        transform: translate(13px, -17px) rotate(5deg);
    }

    50% {
        transform: translate(-7px, -28px) rotate(12deg);
    }

    75% {
        transform: translate(-17px, -10px) rotate(-5deg);
    }

    100% {
        transform: translate(0, 0) rotate(-8deg);
    }
}

@media (max-width: 750px) {
    .hero {
        height: 350px;
        padding: 30px 22px;
    }

    .hero-content {
        max-width: 100%;
    }

    .hero-title {
        font-size: 34px;
    }

    .hero-description {
        max-width: 85%;
        font-size: 12px;
    }

    .floating-item {
        width: 48px;
        height: 48px;
        font-size: 25px;
        opacity: 0.75;
    }

    .item-one {
        right: 8%;
        top: 5%;
    }

    .item-two {
        right: 5%;
        top: 70%;
    }

    .item-three {
        right: 28%;
        top: 78%;
    }

    .item-four, .item-five {
        display: none;
    }
}

@media (prefers-reduced-motion: reduce) {
    .floating-item {
        animation: none;
    }
}

</style>
</head>

<body>

<div class="hero">

    <div class="fashion-decoration">

        <div class="floating-item item-one">👗</div>
        <div class="floating-item item-two">👜</div>
        <div class="floating-item item-three">👚</div>
        <div class="floating-item item-four">👖</div>
        <div class="floating-item item-five">🧥</div>

    </div>

    <div class="hero-content">

        <div class="hero-kicker">
            INTELLIGENCE BEHIND EVERY REVIEW
        </div>

        <div class="hero-title">
            Understand customers.<br>
            Improve every <span>experience.</span>
        </div>

        <div class="hero-description">
            Transform clothing reviews into meaningful insights
            with Machine Learning and Natural Language Processing.
        </div>

    </div>

</div>

</body>
</html>
"""

components.html(
    hero_component,
    height=355,
    scrolling=False
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def show_empty_state(message):
    st.markdown(
        f'<div class="empty-state">{html.escape(message)}</div>',
        unsafe_allow_html=True
    )


def show_success_message(message):
    st.markdown(
        f'<div class="success-message">{html.escape(message)}</div>',
        unsafe_allow_html=True
    )


# =========================================================
# HEADER
# =========================================================

left, right = st.columns([2, 1])

with left:
    st.markdown(
        '<div class="brand">Review<span>IQ</span> ✦</div>',
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        '<div class="nav-label">AI PRODUCT REVIEW INTELLIGENCE</div>',
        unsafe_allow_html=True
    )


# =========================================================
# REVIEW INPUT
# =========================================================

st.markdown("""
<div class="section-kicker">START YOUR ANALYSIS</div>
<div class="section-title">Enter a customer review</div>
<div class="section-description">
    Analyze one review and explore its insights across four separate slides.
</div>
""", unsafe_allow_html=True)

with st.container(border=True):

    review = st.text_area(
        "CUSTOMER REVIEW",
        placeholder="Example: The fabric quality is amazing and the dress is comfortable, but the price is too high...",
        height=120,
        key="main_review"
    )

    if st.button("✦  Analyze Review", use_container_width=True):

        if not review.strip():

            show_empty_state(
                "Please enter a customer review first."
            )

        else:

            with st.spinner("Analyzing your review..."):

                sentiment, confidence = predict_sentiment(review)
                aspects = analyze_aspects(review)
                keywords = extract_keywords(review)

                st.session_state.analysis_results = {
                    "review": review,
                    "sentiment": sentiment,
                    "confidence": confidence,
                    "aspects": aspects,
                    "keywords": keywords
                }

                st.session_state.summary_results = None

            st.session_state.active_slide = "01 Sentiment"
            show_success_message("Review analyzed successfully!")


# =========================================================
# SLIDE NAVIGATION
# =========================================================

st.markdown("""
<div class="section-kicker">YOUR INSIGHTS</div>
<div class="section-title">Analysis dashboard</div>
<div class="section-description">
    Select a section to explore your results.
</div>
""", unsafe_allow_html=True)

slides = [
    "01 Sentiment",
    "02 Aspects",
    "03 Keywords",
    "04 Summary"
]

selected_slide = st.radio(
    "SELECT ANALYSIS",
    slides,
    horizontal=True,
    key="active_slide",
    label_visibility="collapsed"
)


# =========================================================
# SLIDE 1: SENTIMENT ANALYSIS
# =========================================================

if selected_slide == "01 Sentiment":

    st.markdown("""
    <div class="section-kicker">SLIDE 01 / 04</div>
    <div class="section-title">Sentiment Analysis</div>
    <div class="section-description">
        Discover the overall emotion expressed by the customer.
    </div>
    """, unsafe_allow_html=True)

    results = st.session_state.analysis_results

    if results is None:

        show_empty_state(
            "Analyze a review first to discover its sentiment."
        )

    else:

        sentiment = results["sentiment"]
        confidence = results["confidence"]

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.markdown(
                    '<div class="metric-label">PREDICTED SENTIMENT</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="metric-value">{html.escape(str(sentiment))}</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="metric-description">Overall customer opinion</div>',
                    unsafe_allow_html=True
                )

        with col2:

            with st.container(border=True):

                st.markdown(
                    '<div class="metric-label">MODEL CONFIDENCE</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="metric-value">{confidence:.2f}%</div>',
                    unsafe_allow_html=True
                )

                st.progress(
                    max(0.0, min(float(confidence) / 100, 1.0))
                )

                st.markdown(
                    '<div class="metric-description">Estimated prediction probability</div>',
                    unsafe_allow_html=True
                )

        st.markdown("### Analyzed review")

        with st.container(border=True):
            st.write(results["review"])


# =========================================================
# SLIDE 2: ASPECT ANALYSIS
# =========================================================

elif selected_slide == "02 Aspects":

    st.markdown("""
    <div class="section-kicker">SLIDE 02 / 04</div>
    <div class="section-title">Product Aspect Analysis</div>
    <div class="section-description">
        Explore customer opinions about individual product features.
    </div>
    """, unsafe_allow_html=True)

    results = st.session_state.analysis_results

    if results is None:

        show_empty_state(
            "Analyze a review first to see its product aspects."
        )

    elif results["aspects"]:

        aspects = list(results["aspects"].items())
        aspect_columns = st.columns(3)

        for index, (aspect, sentiment) in enumerate(aspects):

            with aspect_columns[index % 3]:

                aspect_card = textwrap.dedent(f"""
                    <div class="aspect-card">
                        <div class="aspect-name">
                            {html.escape(str(aspect).upper())}
                        </div>
                        <div class="aspect-value">
                            {html.escape(str(sentiment))}
                        </div>
                    </div>
                """).strip()

                st.markdown(
                    aspect_card,
                    unsafe_allow_html=True
                )

    else:

        show_empty_state(
            "No recognized product aspects were found in this review."
        )


# =========================================================
# SLIDE 3: KEYWORD EXTRACTION
# =========================================================

elif selected_slide == "03 Keywords":

    st.markdown("""
    <div class="section-kicker">SLIDE 03 / 04</div>
    <div class="section-title">Important Keywords</div>
    <div class="section-description">
        Discover the words and phrases that stand out in customer feedback.
    </div>
    """, unsafe_allow_html=True)

    results = st.session_state.analysis_results

    if results is None:

        show_empty_state(
            "Analyze a review first to extract its keywords."
        )

    elif results["keywords"]:

        with st.container(border=True):

            st.markdown("**KEYWORDS IDENTIFIED**")

            chips = "".join(
                f'<span class="keyword-chip">{html.escape(str(word))}</span>'
                for word in results["keywords"]
            )

            st.markdown(chips, unsafe_allow_html=True)

            st.markdown("**SOURCE REVIEW**")
            st.write(results["review"])

    else:

        show_empty_state(
            "No important keywords were found."
        )


# =========================================================
# SLIDE 4: REVIEW SUMMARY
# =========================================================

elif selected_slide == "04 Summary":

    st.markdown("""
    <div class="section-kicker">SLIDE 04 / 04</div>
    <div class="section-title">Customer Review Summary</div>
    <div class="section-description">
        Bring multiple customer opinions together into a concise summary.
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):

        multiple_reviews = st.text_area(
            "MULTIPLE CUSTOMER REVIEWS",
            placeholder="Paste multiple reviews here. Separate each review with a new line.",
            height=180,
            key="summary_input"
        )

        if st.button("✦  Generate Summary", use_container_width=True):

            reviews_list = [
                line.strip()
                for line in multiple_reviews.split("\n")
                if line.strip()
            ]

            if not reviews_list:

                show_empty_state(
                    "Please enter at least one customer review."
                )

            else:

                with st.spinner("Generating review summary..."):

                    summary = summarize_reviews(
                        reviews_list,
                        top_n=3
                    )

                st.session_state.summary_results = summary

    if st.session_state.summary_results is not None:

        st.markdown("### Summary results")

        if st.session_state.summary_results:

            for index, sentence in enumerate(
                st.session_state.summary_results,
                start=1
            ):

                with st.container(border=True):

                    st.markdown(f"**INSIGHT {index:02d}**")
                    st.write(sentence)

        else:

            show_empty_state(
                "No summary could be generated."
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    REVIEWIQ ✦ BUILT WITH MACHINE LEARNING & NLP
    <br><br>
    TURNING CUSTOMER VOICES INTO PRODUCT INTELLIGENCE.
</div>
""", unsafe_allow_html=True)
