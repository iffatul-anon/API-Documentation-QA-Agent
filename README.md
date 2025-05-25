# API-Documentation-QA-Agent
This Al agent can answer natural language questions about a specific API, using its official documentation as the knowledge base. The agent use vector database embeddings to retrieve relevant context from the documentation before generating an answer with a Large Language Model (LLM).

## 🚀 Features
* 📚 Ingests API documentation (Markdown, text, or HTML)
* ✂️ Chunks and embeds documentation using a semantic model
* 🧠 Stores embeddings in a vector database for semantic search
* 🔍 Retrieves relevant context based on user queries
* 💬 Answers user questions using a Retrieval-Augmented Generation (RAG) pattern
* 🧾 CLI interface (optionally extendable to Streamlit or Gradio)
* ✅ Answers grounded in real documentation (no hallucinations)

## 🧪 How It Works
**Step 1: Data Preparation**
* Load and parse documentation files
* Chunk them into meaningful segments (e.g., sections, paragraphs)

**Step 2: Embedding & Storage**
* Generate vector embeddings for each chunk using your chosen model
* Store chunks and embeddings in the vector database

**Step 3: Q&A Loop**
* Accept natural language question from user
* Embed the question and perform semantic search in the vector DB
* Retrieve top-k relevant documentation chunks
* Construct a prompt with user question + retrieved context
* Send prompt to LLM and return answer

## 🧠 Design Highlights
*   **RAG Pattern:** Combines retrieval and generation for grounded responses
*   **Modularity:** Swap out embedding models, vector DBs, or LLMs easily
*   **Efficiency:** Works locally with fast sentence transformers or via cloud APIs
*   **Transparency:** Context shown in logs or UI to ensure traceability

## 📁 Project Structure
```bash
api-docs-qa-agent/
│
├── data/                    # API documentation files
├── scripts/                 # Scripts for ingestion, embedding, retrieval
│   ├── embed_docs.py
│   └── query_agent.py
├── main.py                  # interface to interact with the agent
├── requirements.txt
└── README.md
```

## 🛠️ Setup Instructions

1. **Clone the repository**
```bash
git clone [repository-url]
cd api-docs-qa-agent
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key
```

4. **Configure documentation sources**
Edit `config.json` to specify your API documentation URLs and other settings:
```json
{
    "documentation_urls": [
        "https://your-api-docs-url"
    ]
}
```

5. **Ingest documentation**
```bash
python scripts/ingest_docs.py
```

6. **Run the application**
```bash
streamlit run app/main.py
```

## 💡 Usage Examples

1. **Basic API Questions**
```
Q: "What are the main features of this API?"
Q: "How do I authenticate with the API?"
Q: "Show me example code for making a GET request"
```

2. **Documentation Updates**
The agent automatically processes new documentation when you:
```bash
python scripts/ingest_docs.py
```

## 🔧 Configuration

The `config.json` file allows you to customize:
- Documentation sources
- Embedding model settings
- Chunking parameters
- Vector database configuration


## ✅ Deliverables
*   ✅ Complete source code
*   ✅ `requirements.txt`
*   ✅ Documentation & instructions
*   ✅ Modular architecture: easy to switch models or vector DBs
*   ✅ Sample test cases for questions