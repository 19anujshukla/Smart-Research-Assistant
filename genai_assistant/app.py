import streamlit as st
import os
from dotenv import load_dotenv
import cohere
import re

from utils.parser import extract_text
from utils.qa import create_vector_store, get_relevant_chunks, ask_with_context
from utils.challenge import generate_questions, evaluate_answer

# Load API key
load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Page config
st.set_page_config(page_title="Smart Research Assistant", page_icon="📄", layout="wide")

# Stylish Sidebar
with st.sidebar:
    st.markdown("""
    <style>
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 10px;
    }
    .sidebar-sub {
        font-size: 14px;
        color: #999;
        text-align: center;
        margin-bottom: 20px;
    }
    .emoji-box {
        text-align: center;
        font-size: 40px;
        margin-bottom: 10px;
    }
    .pill {
        background-color: #f0f2f6;
        padding: 6px 10px;
        border-radius: 20px;
        display: inline-block;
        font-size: 13px;
        margin: 4px;
        color: #333;
    }
    </style>
    <div class="emoji-box">🧠📚🤖</div>
    <div class="sidebar-title">GenAI Research Buddy</div>
    <div class="sidebar-sub">by Anuj Kumar Shukla</div>
    """, unsafe_allow_html=True)

    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Cohere_logo.svg/2560px-Cohere_logo.svg.png", use_column_width=True)

    st.markdown("""
    <div class="pill">Summarize PDFs</div>
    <div class="pill">Generate Questions</div>
    <div class="pill">Get Feedback</div>
    <div class="pill">Evaluate Answers</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.info("Upload a document to get started.")

# Title
st.title("📄 Smart Assistant for Research Summarization")
st.write("Upload any document and explore AI-powered summaries, Q&A, and personalized challenges.")

# Upload and Extraction
col1, col2 = st.columns([1, 2])
with col1:
    uploaded_file = st.file_uploader("📤 Upload PDF or TXT", type=["pdf", "txt"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]
    try:
        raw_text = extract_text(uploaded_file, file_type)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    st.success("✅ Document successfully extracted!")

    with st.spinner("🔄 Generating summary..."):
        prompt = f"Summarize the following document in no more than 150 words:\n\n{raw_text[:3000]}"
        summary = co.generate(model="command-r-plus", prompt=prompt, max_tokens=300, temperature=0.3).generations[0].text.strip()

    with col2:
        st.subheader("📑 Auto Summary")
        st.info(summary)

    with st.expander("📄 View Full Extracted Text"):
        st.text_area("Document Text", raw_text, height=300)

    # Q&A
    st.subheader("💬 Ask Questions (Chat Mode)")
    embeddings, doc_chunks = create_vector_store(raw_text)
    user_question = st.text_input("🔎 Type your question here:")

    if user_question:
        with st.spinner("🔍 Finding answer..."):
            relevant_chunks = get_relevant_chunks(user_question, embeddings, doc_chunks)
            answer = ask_with_context(user_question, relevant_chunks)
        st.markdown("**Answer:**")
        st.success(answer)

        with st.expander("🧠 Context Used"):
            st.write(relevant_chunks)

    # Challenge Me Mode
    st.subheader("🧠 Challenge Me Mode")
    if "challenge_questions" not in st.session_state:
        st.session_state.challenge_questions = []
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "feedback" not in st.session_state:
        st.session_state.feedback = {}

    if st.button("🔁 Generate 3 Challenge Questions"):
        with st.spinner("Generating questions..."):
            st.session_state.challenge_questions = generate_questions(raw_text)[:3]
            st.session_state.answers = {}
            st.session_state.feedback = {}

    if st.session_state.challenge_questions:
        for i, question in enumerate(st.session_state.challenge_questions):
            st.markdown(f"**Q{i+1}: {question}**")
            with st.form(key=f"form_{i}"):
                user_input = st.text_area("✏️ Your Answer:", key=f"user_answer_{i}")
                submitted = st.form_submit_button("Submit Answer")

                if submitted and user_input.strip():
                    with st.spinner("Evaluating..."):
                        feedback = evaluate_answer(question, user_input, raw_text)
                        st.session_state.answers[i] = user_input
                        st.session_state.feedback[i] = feedback

            if i in st.session_state.feedback:
                st.success("✅ Feedback:")
                st.markdown(st.session_state.feedback[i])
