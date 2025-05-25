import streamlit as st
from scripts.query_agent import generate_combined_response
from scripts.load_docs import scrape_url
from scripts.chunk_docs import chunk_text
from scripts.embed_retrive_docs import embed_and_save_to_vectordb
from scripts.conversation_load_and_save import load_conversation_history, save_conversation_history

def main():
    st.title("📘 API Documentation Q&A Agent")

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
                    text = scrape_url(url_input)
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
