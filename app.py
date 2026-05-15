import streamlit as st
import sqlite3
import hashlib
from textblob import TextBlob
import pandas as pd

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS history (
    username TEXT,
    question TEXT,
    answer TEXT,
    score REAL
)
""")

conn.commit()

# ---------------- HELPERS ----------------
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    return c.fetchone()

def add_user(username, password):
    try:
        c.execute("INSERT INTO users VALUES (?,?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

def save_history(username, q, a, score):
    c.execute("INSERT INTO history VALUES (?,?,?,?)",
              (username, q, a, score))
    conn.commit()

def get_history(username):
    c.execute("SELECT question, answer, score FROM history WHERE username=?",
              (username,))
    return c.fetchall()

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

# ---------------- UI SETUP ----------------
st.set_page_config(page_title="AI Interview SaaS", layout="centered")

st.title("🤖 AI Interview SaaS Platform")
st.caption("Professional Interview Practice System")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- AUTH PAGE ----------------
def auth():
    st.subheader("🔐 Login / Signup")

    option = st.radio("Choose", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Create Account"):
            if add_user(username, password):
                st.success("Account created! Please login.")
            else:
                st.error("User already exists")

    if option == "Login":
        if st.button("Login"):
            if check_user(username, password):
                st.session_state.user = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# ---------------- MAIN APP ----------------
def app():
    st.sidebar.write(f"👤 Logged in as: {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    questions = [
        "Tell me about yourself",
        "Why do you want this job?",
        "What are your strengths?"
    ]

    st.title("🧠 Interview Practice")

    scores = []

    for q in questions:
        st.subheader(q)
        ans = st.text_area("Your Answer", key=q)

        if st.button(f"Submit - {q}"):
            if ans:
                score, label = analyze(ans)

                save_history(st.session_state.user, q, ans, score)

                st.success(label)
                st.info(f"Score: {round(score,2)}/100")

    # ---------------- DASHBOARD ----------------
    data = get_history(st.session_state.user)

    if data:
        df = pd.DataFrame(data, columns=["Question", "Answer", "Score"])

        st.subheader("📊 Your Performance Dashboard")

        st.metric("Average Score", round(df["Score"].mean(), 2))

        st.bar_chart(df.set_index("Question")["Score"])

        st.subheader("📜 History")
        st.dataframe(df)

# ---------------- FLOW ----------------
if st.session_state.user is None:
    auth()
else:
    app()
