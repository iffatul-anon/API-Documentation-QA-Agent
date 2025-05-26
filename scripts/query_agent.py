"""
This module implements the core Q&A functionality using the Phi framework and Groq LLM.

It handles the integration between the vector database search results and the LLM,
implementing a Retrieval-Augmented Generation (RAG) pattern to provide accurate
responses based on the API documentation while maintaining conversation context.

Environment Variables Required:
    GROQ_API_KEY: API key for accessing the Groq LLM service

Dependencies:
    - phi-agent
    - python-dotenv
    - groq-sdk
"""

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.googlesearch import GoogleSearch
from dotenv import load_dotenv
from scripts.embed_retrive_docs import search_vectordb
from typing import List, Dict, Tuple, Optional
import logging

# Initialize logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize the AI agent with Groq LLM
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    name="API Documentation Q&A Agent",
    role="Provide accurate and detailed responses for API documentation queries.",
    description="A virtual assistant specializing in API documentation Q&A.",
    instructions=[
        "Provide concise and accurate answers based on the documentation.",
        "If the answer is not found, recommend searching further or checking the official API docs.",
        "Always use markdown formatting when listing endpoints or steps.",
        "If the user does not ask for specific information, act like a chatbot and engage in casual conversation.",
    ],
    tools=[GoogleSearch()],
    markdown=True,
)

def generate_combined_response(
    user_input: str,
    history: List[Dict[str, str]]
) -> Tuple[str, List[str]]:
    """
    Generate a response to the user's query using RAG pattern.

    This function combines the conversation history with relevant documentation
    context to generate an informed response. It uses vector similarity search
    to find relevant documentation snippets and feeds them to the LLM along
    with the conversation history.

    Args:
        user_input (str): The user's current question or message
        history (List[Dict[str, str]]): List of previous conversation entries,
            where each entry is a dict with 'role' and 'message' keys

    Returns:
        Tuple[str, List[str]]: A tuple containing:
            - The generated response text
            - A list of any additional messages or warnings (currently unused)

    Example:
        >>> history = [
        ...     {"role": "user", "message": "How do I authenticate?"},
        ...     {"role": "assistant", "message": "You need an API key..."}
        ... ]
        >>> response, messages = generate_combined_response(
        ...     "Where do I find my API key?",
        ...     history
        ... )
        >>> print(response)
    """
    # Limit history to prevent context window overflow
    MAX_HISTORY = 5
    formatted_history = "\n".join(
        [f"{chat['role'].capitalize()}: {chat['message']}" for chat in history[-MAX_HISTORY:]]
    )

    context_chunks = search_vectordb(user_input, top_k=5)
    if not context_chunks:
        kb_context = "No relevant documentation found. Please check the official API docs."
    else:
        kb_context = "\n".join(context_chunks)

    prompt = (
        f"You are an API documentation Q&A Agent. Use the following information:\n\n"
        f"1. Conversation History:\n{formatted_history}\n\n"
        f"2. Knowledge Base Context:\n{kb_context}\n\n"
        f"3. User Query:\n{user_input}\n"
    )

    response = agent.run(prompt).content

    return response, []