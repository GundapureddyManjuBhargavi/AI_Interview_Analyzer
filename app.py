import streamlit as st
from textblob import TextBlob
import plotly.express as px
import pandas as pd

# Page Settings
st.set_page_config(
    page_title="AI Interview Analyzer",
    layout="centered"
)

# Title
st.title("🎯 AI Interview Analyzer")

# Sidebar
st.sidebar.header("About Project")
st.sidebar.write(
    "This AI project analyzes interview answers using NLP "
    "and generates confidence scores with analytics dashboard."
)

# Questions
questions = [
    "Tell me about yourself",
    "Why do you want this job?",
    "What are your strengths?"
]

# Positive Keywords
positive_words = [
    "confident",
    "hardworking",
    "passionate",
    "teamwork",
    "leadership",
    "problem solving",
    "communication",
    "dedicated",
    "motivated",
    "creative",
    "analytical",
    "technical",
    "responsible",
    "focused"
]

# Variables
scores = []
question_list = []

answered = 0

# Progress Bar
progress = st.progress(0)

# Questions Loop
for question in questions:

    st.subheader(question)

    answer = st.text_area(f"Answer for: {question}")

    if answer:

        answered += 1

        # NLP Analysis
        blob = TextBlob(answer)

        sentiment = blob.sentiment.polarity

        # Bonus Score
        bonus = 0

        for word in positive_words:
            if word in answer.lower():
                bonus += 0.1

        sentiment += bonus

        # Final Score
        score = (sentiment + 1) * 50

        scores.append(score)
        question_list.append(question)

        # Result Messages
        if sentiment > 0.3:
            st.success("✅ Positive and Confident Answer")

        elif sentiment > 0:
            st.info("🙂 Slightly Positive Answer")

        elif sentiment > -0.2:
            st.warning("⚠️ Neutral Answer")

        else:
            st.error("❌ Negative or Low Confidence Answer")

    progress.progress(answered / len(questions))

# Final Report
if st.button("Generate Final Report"):

    average_score = sum(scores) / len(scores)

    st.header("📊 Final Interview Report")

    st.write(f"Final Score: {average_score:.2f}/100")

    # Performance Message
    if average_score > 75:

        st.success("🌟 Excellent Interview Performance")

    elif average_score > 50:

        st.warning("👍 Good Performance, Needs Improvement")

    else:

        st.error("⚠️ Low Confidence Performance")

    # AI Feedback
    st.subheader("🤖 AI HR Feedback")

    if average_score > 75:

        st.write("""
        ✔ Strong communication skills  
        ✔ Excellent confidence level  
        ✔ Professional interview responses  
        ✔ Strong technical mindset  
        """)

    elif average_score > 50:

        st.write("""
        ✔ Good communication skills  
        ✔ Positive attitude detected  
        ✔ Improve confidence slightly  
        ✔ Add more technical details  
        """)

    else:

        st.write("""
        ✔ Needs confidence improvement  
        ✔ Practice interview communication  
        ✔ Improve technical explanation skills  
        """)

    # Create DataFrame
    df = pd.DataFrame({
        "Question": question_list,
        "Score": scores
    })

    # Bar Chart
    st.subheader("📈 Question-wise Performance")

    fig = px.bar(
        df,
        x="Question",
        y="Score",
        title="Interview Performance Analysis"
    )

    st.plotly_chart(fig)

    # Pie Chart
    st.subheader("🥧 Performance Distribution")

    performance_data = pd.DataFrame({
        "Category": ["Score", "Remaining"],
        "Value": [average_score, 100 - average_score]
    })

    pie_chart = px.pie(
        performance_data,
        names="Category",
        values="Value",
        title="Overall Interview Score"
    )

    st.plotly_chart(pie_chart)

# Footer
st.markdown("---")
st.write("Developed using Python, Streamlit, NLP, Plotly and TextBlob")