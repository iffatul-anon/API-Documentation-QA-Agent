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

# Load environment variables from .env file
load_dotenv()

# Initialize the AI agent with Groq LLM
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),

    name = "API Documentation Q&A Agent",

    role = (
        "An intelligent assistant designed to answer technical questions using scraped and embedded API documentation. "
        "Capable of interpreting developer queries, summarizing endpoints, and guiding users through API usage."
    ),

    description = (
        "An LLM-powered virtual assistant trained to help developers understand and use API documentation effectively. "
        "Specialized in retrieving relevant content and responding in a clear, developer-friendly format."
    ),

    instructions = [
        "Use the provided documentation context to answer queries accurately and concisely.",
        "Respond in markdown format with code blocks, bullet points, or numbered lists when appropriate.",
        "Include relevant endpoints, parameters, or example responses where possible.",
        "If information is missing, acknowledge it and suggest checking the original documentation or using the search tool.",
        "When the user asks a general or unclear question, guide them toward clarification or respond conversationally.",
        "Avoid guessing. If the context does not support a confident answer, explain that clearly.",
        "When the user does not ask about the documentation, switch to friendly chatbot mode and engage casually.",
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
        "You are an expert API documentation assistant. Use the following information to answer the user's query:\n\n"
        f"## Conversation History:\n{formatted_history}\n\n"
        f"## Retrieved Documentation Snippets:\n{kb_context}\n\n"
        f"## User Question:\n{user_input}\n\n"
        "Answer concisely using markdown. Include relevant endpoints, code examples, or references. "
        "If the answer is unclear from the context, suggest checking the official documentation or performing a web search."
    )

    response = agent.run(prompt).content

    return response, []