import streamlit as st
from textblob import TextBlob
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Interview Coach", layout="centered")

# ---------------- FAKE DATABASE (SESSION STORAGE) ----------------
if "users" not in st.session_state:
    st.session_state.users = {}   # stores username:password

if "login_user" not in st.session_state:
    st.session_state.login_user = None

if "history" not in st.session_state:
    st.session_state.history = {}

# ---------------- AUTH FUNCTIONS ----------------
def signup(username, password):
    if username in st.session_state.users:
        return False, "User already exists"
    st.session_state.users[username] = password
    st.session_state.history[username] = []
    return True, "Account created successfully"

def login(username, password):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.login_user = username
        return True
    return False

# ---------------- ANALYSIS ----------------
def analyze(answer):
    polarity = TextBlob(answer).sentiment.polarity
    score = (polarity + 1) * 50

    if score >= 75:
        label = "Excellent 🚀"
    elif score >= 60:
        label = "Good 👍"
    elif score >= 40:
        label = "Average ⚠️"
    else:
        label = "Needs Improvement ❌"

    return score, label

# ---------------- LOGIN PAGE ----------------
def auth_page():
    st.title("🔐 AI Interview Coach")

    option = st.radio("Choose option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Create Account"):
            ok, msg = signup(username, password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    if option == "Login":
        if st.button("Login"):
            if login(username, password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ---------------- MAIN APP ----------------
def main_app():

    st.title("🤖 AI Interview Coach (Pro Version)")
    st.caption(f"Welcome {st.session_state.login_user}")

    questions = [
        "Tell me about yourself",
        "Why do you want this job?",
        "What are your strengths?"
    ]

    if st.button("Logout"):
        st.session_state.login_user = None
        st.rerun()

    if st.session_state.login_user not in st.session_state.history:
        st.session_state.history[st.session_state.login_user] = []

    scores = []

    st.markdown("---")

    for q in questions:
        st.subheader(q)
        ans = st.text_area("Your Answer", key=q)

        if st.button(f"Submit {q}"):
            if ans.strip():
                score, label = analyze(ans)

                st.success(label)
                st.info(f"Score: {round(score,2)}")

                st.session_state.history[st.session_state.login_user].append({
                    "question": q,
                    "answer": ans,
                    "score": score
                })

    # ---------------- DASHBOARD ----------------
    user_history = st.session_state.history[st.session_state.login_user]

    if len(user_history) > 0:
        st.markdown("---")
        st.subheader("📊 Your Report")

        df = pd.DataFrame(user_history)

        final_score = df["score"].mean()

        st.metric("Final Score", f"{final_score:.2f}/100")

        st.bar_chart(df.set_index("question")["score"])

        st.subheader("📜 History")
        st.dataframe(df)

# ---------------- FLOW ----------------
if st.session_state.login_user is None:
    auth_page()
else:
    main_app()
