from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.googlesearch import GoogleSearch
from dotenv import load_dotenv
from scripts.embed_retrive_docs import search_vectordb

load_dotenv()

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
    tools=[
        GoogleSearch()
    ],
    markdown=True,
)

def generate_combined_response(user_input, history):
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
