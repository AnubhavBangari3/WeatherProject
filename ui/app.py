import sys
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# Add root folder and app folder into sys.path
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "app"))

from agent_graph import agent_app
from rag import ingest_pdf_into_qdrant

import streamlit as st





st.set_page_config(
    page_title="Weather + PDF Agent",
    layout="centered",
)

st.title("Weather + PDF RAG Agent")

st.markdown(
    """
This app uses **LangGraph + LangChain + DeepSeek + Qdrant** to:
- Fetch real-time **weather** data.
- Answer questions from a **PDF** using RAG.
"""
)

if st.button("Ingest / Rebuild PDF Vector Store"):
    with st.spinner("Ingesting PDF into Qdrant..."):
        n_chunks = ingest_pdf_into_qdrant(force_rebuild=True)
    st.success(f"Ingested {n_chunks} chunks from PDF into Qdrant ✅")

st.markdown("---")

user_input = st.text_input("Ask me something:", placeholder="e.g. What's the weather in London? Or: Explain chapter 2 from the PDF")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Send") and user_input:
    st.session_state.chat_history.append(("user", user_input))

    with st.spinner("Thinking..."):
        state = {"input": user_input, "route": "unknown", "answer": ""}
        result = agent_app.invoke(state)
        answer = result["answer"]
        route = result["route"]

    st.session_state.chat_history.append(("assistant", answer))
    st.session_state.chat_history.append(("meta", f"[Handled via: {route.upper()}]"))

# Display history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    elif role == "assistant":
        st.markdown(f"**Assistant:** {msg}")
    else:
        st.caption(msg)
