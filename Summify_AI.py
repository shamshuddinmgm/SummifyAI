# Remove nest_asyncio.apply() from the code
# import nest_asyncio  # Remove this line
# nest_asyncio.apply()  # Remove this line

import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from transformers import pipeline
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import logging

# Download necessary resources for sentiment analysis
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Cache sentiment analysis model
@st.cache_resource
def get_sentiment_pipeline():
    return pipeline("sentiment-analysis", model="./models/distilbert-sentiment")

sentiment_pipeline = get_sentiment_pipeline()

# Cache BART summarization model
@st.cache_resource
def get_bart_pipeline():
    return pipeline("summarization", model="./models/distilbart-cnn-12-6")

bart_pipeline = get_bart_pipeline()

# Cache zero-shot classification model
@st.cache_resource
def get_classification_pipeline():
    return pipeline("zero-shot-classification", model="./models/bart-large-mnli")

classification_pipeline = get_classification_pipeline()

# Function to load dataset
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, sheet_name="Sheet1")
            return df
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
            return None
    return None

# Function to generate a word cloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='#1E1E1E', colormap='coolwarm').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    return fig

# Function to extract sentiment words
def extract_sentiment_words(text):
    words = text.split()
    positive_words = [word for word in words if sia.polarity_scores(word)['compound'] > 0.2]
    negative_words = [word for word in words if sia.polarity_scores(word)['compound'] < -0.2]
    return positive_words[:10], negative_words[:10]  # Show top 10 of each

# Custom CSS for styling
st.markdown(
    """
    <style>
    .title {
        background: linear-gradient(#634e6e, #2e4373, #9bcf76);
        color: white;
        padding: 10px;
        text-align: center;
        font-size: 28px;
        border-radius: 10px;
    }
    .result-box {
        background: linear-gradient(135deg, #be94f2, #008268);
        padding: 7px;
        border-radius: 7px;
        margin-top: 7px;
    }
    .positive-title {
        color: #28a745;
        font-size: 18px;
        font-weight: bold;
    }
    .negative-title {
        color: #dc3545;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with Logo
logo_path = "logo.png"
if os.path.exists(logo_path):  
    st.sidebar.image(logo_path, use_container_width=True)

st.sidebar.title("Navigation")

# File Upload Section
st.sidebar.subheader("Step 1: Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

df = load_data(uploaded_file)

if df is not None and all(col in df.columns for col in ["title", "text", "category", "summary", "published_date", "top_image", "section"]):
    st.sidebar.subheader("Step 2: Select an Article")
    article_options = ["SELECT"] + df["title"].dropna().tolist()
    selected_title = st.sidebar.selectbox("Choose an article", article_options)
    
    if selected_title == "SELECT":
        st.sidebar.warning("Please select an article to proceed.")
    else:
        st.sidebar.subheader("Step 3: Choose an NLP Task")
        nlp_task = st.sidebar.selectbox("NLP Task", ["Text Summarization", "Text Classification", "Sentiment Analysis"])
        run_button = st.sidebar.button("Run Task")
        
        article = df[df["title"] == selected_title].iloc[0]
        
        if run_button:
            st.markdown('<div class="result-box">', unsafe_allow_html=True)

            # Category Handling and Classification
            category = article.get('category', '')
            if pd.isna(category) or category.strip() == "":
                # If category is missing or blank, classify the article
                categories = ["Sports", "Politics", "Technology", "Health", "Entertainment", "Business"]
                result = classification_pipeline(article['text'], candidate_labels=categories)
                predicted_category = result['labels'][0]
                st.write(f"Predicted Category: {predicted_category}")
            else:
                st.write(f"Category: {category}")

            # NLP Task Execution: Summarization
            if nlp_task == "Text Summarization":
                st.subheader("Summarization Result")
                summary_text = article.get("summary", "")
                if pd.isna(summary_text):  # Handle NaN values
                    summary_text = ""
                if summary_text.strip() == "":
                    text_content = article.get("text", "")
                    if text_content:
                        # Limit text length to prevent issues with token limits
                        truncated_text = " ".join(text_content.split()[:500])
                        generated = bart_pipeline(truncated_text, max_length=150, min_length=40, do_sample=False)
                        generated_summary = generated[0]['summary_text']
                        st.write(generated_summary)
                    else:
                        st.write("No content available for summarization.")
                else:
                    st.write(summary_text)
            
            # NLP Task Execution: Sentiment Analysis
            elif nlp_task == "Sentiment Analysis":
                st.subheader("Sentiment Analysis Result")
                sentiment_text = " ".join(article.get("text", "").split()[:100])
                sentiment = sentiment_pipeline(sentiment_text) if sentiment_text else [{"label": "N/A", "score": 0.0}]
                st.write(f"Sentiment: {sentiment[0]['label']} (Confidence: {sentiment[0]['score']:.2f})")

                # Extract and display sentiment words
                pos_words, neg_words = extract_sentiment_words(article.get("text", ""))
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<span class="positive-title">Positive Words ({len(pos_words)})</span>', unsafe_allow_html=True)
                    st.write(", ".join(pos_words) if pos_words else "No significant positive words found.")
                with col2:
                    st.markdown(f'<span class="negative-title">Negative Words ({len(neg_words)})</span>', unsafe_allow_html=True)
                    st.write(", ".join(neg_words) if neg_words else "No significant negative words found.")
                st.markdown("</div>", unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)

else:
    if uploaded_file:
        st.sidebar.error("Dataset missing required columns.")

# Main Content
st.markdown('<div class="title"><em><b>News Article Classification and Summarization</div></b></em>', unsafe_allow_html=True)

if df is not None and selected_title != "SELECT":
    st.subheader("Selected Article")
    st.write(f"**Title:** {article.get('title', 'N/A')}")
    st.write(f"**Published Date:** {article.get('published_date', 'N/A')}")
    st.write(f"**Category:** {article.get('category', 'N/A')}")
    st.write(f"**Section:** {article.get('section', 'N/A')}")
    
    if article.get("top_image"):
        st.image(article["top_image"], use_container_width=True)
    else:
        st.image("default_image.png", use_container_width=True)
    
    st.write(article.get("text", "No content available."))
    
    # Generate and display word cloud
    st.subheader("Word Cloud of Dataset")
    text_data = " ".join(df["text"].dropna().tolist()[:5000])
    wordcloud_fig = generate_wordcloud(text_data)
    st.pyplot(wordcloud_fig)
