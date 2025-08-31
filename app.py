
import streamlit as st
from rag_pipeline import generate_answer

# Streamlit page setup
st.set_page_config(
    page_title="Lex Fridman Podcast Chatbot",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Lex Fridman Podcast Chatbot")
st.markdown("Ask any question about the Lex Fridman Podcast. Answers are grounded in the podcast transcripts.")

# Chat input
user_question = st.text_input("Enter your question:", "")

if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            answer = generate_answer(user_question)
        st.success("Answer:")
        st.write(answer)
