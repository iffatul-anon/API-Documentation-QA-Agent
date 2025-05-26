"""
API Documentation Q&A Agent - Main Application

This is the main entry point for the API Documentation Q&A Agent application.
It provides a Streamlit-based web interface for users to interact with the
documentation assistant. Users can load API documentation from URLs, ask
questions, and maintain conversation history across sessions.

Features:
- Load and process API documentation from URLs
- Interactive chat interface with conversation history
- Vector-based semantic search for relevant documentation
- LLM-powered responses using RAG pattern
- Persistent conversation history

Usage:
    Run the application using:
    ```bash
    streamlit run main.py
    ```

Dependencies:
    - streamlit
    - All custom modules in scripts/
"""

import streamlit as st
from scripts.query_agent import generate_combined_response
from scripts.load_docs import scrape_and_structure_data
from scripts.chunk_docs import chunk_text
from scripts.embed_retrive_docs import embed_and_save_to_vectordb
from scripts.conversation_load_and_save import load_conversation_history, save_conversation_history
from typing import List, Dict, Optional

def main() -> None:
    """
    Main application function that sets up the Streamlit interface and handles
    the interaction flow.

    The function:
    1. Sets up the main UI components
    2. Handles documentation loading from URLs
    3. Manages conversation state and history
    4. Processes user inputs and displays responses

    No parameters or return values as this is the top-level application function.
    Stores state in st.session_state and handles all UI interactions directly.
    """

    # Sidebar for options
    with st.sidebar:
        if st.button("🧹 Clear Chat History"):
            st.session_state.chat_history.clear()
            save_conversation_history([])
            st.success("Chat history cleared!")

        url_input = st.text_input("Enter API Documentation URL")
        if st.button("Load Docs"):
            with st.spinner("Scraping and processing..."):
                try:
                    text = scrape_and_structure_data(url_input)
                    chunks = chunk_text(text,500,50)
                    embed_and_save_to_vectordb(chunks)
                    st.success(f"{len(chunks)} chunks saved to VectorDB.")
                except Exception as e:
                    st.error(str(e))

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_conversation_history()

    user_input = st.chat_input("Ask me anything about API...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        st.chat_message("user").markdown(user_input)

        with st.spinner("Processing your question..."):
            response_text, _ = generate_combined_response(
                user_input, st.session_state.chat_history
            )

        st.session_state.chat_history.append({"role": "assistant", "message": response_text})
        st.chat_message("assistant").markdown(response_text, unsafe_allow_html=True)

        save_conversation_history(st.session_state.chat_history)

    for chat in st.session_state.chat_history:
        role = "You" if chat["role"] == "user" else "Assistant"
        st.chat_message(chat["role"]).markdown(f"**{role}**: {chat['message']}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()