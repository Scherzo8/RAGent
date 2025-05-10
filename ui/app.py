import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    ))

# To avoid Streamlit file-watching issues with PyTorch, this project disables the watcher explicitly using
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import streamlit as st
from core.agents import route_query
from core.retriever import get_relevant_chunks


st.set_page_config(page_title="RAG Multi-Agent Assistant", layout="wide")

st.title("RAG-Powered Multi-Agent Assistant")

query = st.text_input("Ask me anything:", "")

if query:
    with st.spinner("Thinking..."):
        tool, response = route_query(query)

        st.subheader("Tool Used")
        st.markdown(f"**{tool}**")

        st.subheader("Response")
        st.markdown(response)

        if "LLM" in tool:
            st.subheader("Retrieved Context")
            chunks = get_relevant_chunks(query)

            for i, chunk in enumerate(chunks):
                st.markdown(f"**Chunk {i+1}**: {chunk}")