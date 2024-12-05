import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Setup database connection (SQLite for simplicity)
engine = create_engine("sqlite:///papers.db")

# Function to fetch topics dynamically from the database
def get_topics():
    query = "SELECT DISTINCT prediction FROM papers"
    topics = pd.read_sql(query, engine)
    return topics["prediction"].tolist()

# Function to fetch papers for a given topic
def get_papers_by_topic(topic):
    query = f"""
    SELECT paper_title, paper_abstract, prediction_score 
    FROM papers 
    WHERE prediction = :topic 
    ORDER BY prediction_score DESC
    """
    return pd.read_sql(query, engine, params={"topic": topic})

# Main Streamlit App
st.set_page_config(page_title="Research Topics", layout="wide")

# Streamlit session_state to manage selected topic
if "selected_topic" not in st.session_state:
    st.session_state["selected_topic"] = None

# Index Page: Display Topics
if st.session_state["selected_topic"] is None:
    st.title("Research Topics")

    # Fetch and display topics
    topics = get_topics()
    for topic in topics:
        if st.button(topic):
            st.session_state["selected_topic"] = topic
            st.experimental_rerun()

# Child Page: Display Papers for Selected Topic
else:
    topic = st.session_state["selected_topic"]
    st.title(f"Topic: {topic}")

    # Back Button
    if st.button("Back to Topics"):
        st.session_state["selected_topic"] = None
        st.experimental_rerun()

    # Fetch papers for the selected topic
    papers = get_papers_by_topic(topic)

    # Left Column: Abstract Display
    left_col, center_col, right_col = st.columns([1, 3, 1])

    with left_col:
        st.header("Abstract")
        selected_abstract = st.empty()  # Placeholder for abstract text

    # Center Column: Visualization
    with center_col:
        st.header("Visualization")

        if not papers.empty:
            # Plotly Bar Chart
            fig = px.bar(
                papers,
                x="prediction_score",
                y="paper_title",
                orientation="h",
                text="prediction_score",
                title=f"Papers in {topic}",
                labels={"title": "Paper Title", "prediction_score": "Prediction Score"},
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.write("No papers found for this topic.")

    # Right Column: Top Papers List
    with right_col:
        st.header("Top Papers")
        for i, row in papers.head(10).iterrows():
            if st.button(row["paper_title"]):
                selected_abstract.text(row["paper_abstract"])  # Show abstract in the left pane

