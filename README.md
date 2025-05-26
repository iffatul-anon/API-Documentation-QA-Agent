# API Documentation QA Agent

A lightweight AI agent that answers natural language questions about APIs using their official documentation. It leverages vector embeddings and Retrieval-Augmented Generation (RAG) for accurate, context-aware responses.

---

## 🚀 Features

- 📄 Ingests HTML, Markdown, or text-based API docs  
- ✂️ Chunks and embeds docs using semantic models  
- 🧠 Stores embeddings in LanceDB for fast retrieval  
- 🔍 Retrieves relevant context for user queries  
- 💬 Uses Groq LLM (LLaMA 3) for natural language answers  
- 🧾 Streamlit-based interactive interface  
- 🔁 Maintains basic conversation history for follow-ups  

---

## 🧱 Tech Stack

| Component        | Technology                               | Overview                                                                              |
|------------------|------------------------------------------|---------------------------------------------------------------------------------------|
| Language         | Python                                   | Widely used for AI/ML and rapid prototyping; strong library ecosystem                 |
| LLM              | Groq (LLaMA 3.3 70B Versatile)           | This open-source free LLM model provides high-performance inference for complex queries with minimal latency |
| Agent Framework  | Phidata                                  | Lightweight framework that simplifies building agent-based workflows                  |
| Vector DB        | LanceDB                                  | Chosen for its performance and simplicity; ideal for lightweight, local deployments   |
| Embeddings       | SentenceTransformer (all-MiniLM-L6-v2)      | Offers a strong balance between speed and accuracy for generating semantic embeddings |
| Scraping         | Unstructured Library                     | Parses diverse content types like HTML and Markdown into structured text              |
| Chunking         | LangChain Text Splitter                 | Efficiently handles large documents for optimal embedding and retrieval               |
| UI               | Streamlit                                | Enables fast development of clean, interactive UIs without frontend expertise         |
| History Storage  | JSON                                     | Lightweight and simple method to manage short-term conversational state               |

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/iffatul-anon/API-Documentation-QA-Agent
cd API-Documentation-QA-Agent
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key
```

### 4. Run the Application
```bash
streamlit run main.py
```

---

## 📋 System Requirements

* Python 3.8 or higher
* 1GB free disk space (for vector database storage)
* Active internet connection (for LLM API access)
* Groq API account and key

## 🔧 Dependencies

Core dependencies:
* `streamlit`: Web interface
* `phidata`: LLM agent framework
* `sentence-transformers`: Document embedding
* `lancedb`: Vector database
* `langchain`: Text chunking
* `unstructured`: Document parsing
* `python-dotenv`: Environment management

See `requirements.txt` for complete list of dependencies.

---

## 💡 How It Works
**Step 1: Data Preparation**
* Load and parse documentation files
* Chunk them into meaningful segments (e.g., sections, paragraphs)

**Step 2: Embedding & Storage**
* Generate vector embeddings for each chunk using embedding model
* Store chunks and embeddings in the vector database

**Step 3: Q&A Loop**
* Accept natural language question from user
* Embed the question and perform semantic search in the vector DB
* Retrieve top-k relevant documentation chunks
* Construct a prompt with user question + retrieved context + conversation history
* Send prompt to LLM and return answer

---

## 💡 Usage

### Load Documentation
1. Open the app in your browser.
2. Enter an API documentation URL in the sidebar.
3. Click **Load Docs** to parse and embed content.

### Ask Questions
Examples:
- _"How do I authenticate with the API?"_  
- _"List available endpoints."_  
- _"What parameters does `/users` accept?"_

### Manage Docs
- Use "Clear Chat History" to reset coversation history.

---

## 📁 Project Structure
```
api-docs-qa-agent/
├── data/                  # Vector DB & chat history
├── scripts/               # Core logic: ingestion, embedding, querying
│   ├── chunk_docs.py
│   ├── embed_retrive_docs.py
│   ├── load_docs.py
│   ├── query_agent.py
│   └── conversation_load_and_save.py
├── main.py                # Streamlit UI entry point
├── requirements.txt
└── README.md
```

---

## ⚠️ Limitations

- Best with structured HTML docs (PDFs not supported)
- Conversation history limited (last 5 messages due to prompt size limitations in open-source LLM models)
- Initial load time varies by doc size
- Complex queries may need step-by-step interaction

---

## 🧰 Troubleshooting

| Issue                      | Fix                                                           |
|----------------------------|---------------------------------------------------------------|
| App won't start            | Check Python version, activate venv, verify dependencies      |
| Doc load fails             | Confirm URL accessibility, internet, retry with another URL   |
| No agent response          | Verify API key, internet, and doc loading                     |
| Poor answers               | Rephrase question or load additional docs                     |

---

## 📬 Contact
- Name: Md. Iffatul Islam Anon
- Email: anon35-1065@diu.edu.bd
- Email: iffatulislamanon@gmail.com
- Linkedin: [iffatul-anon](https://www.linkedin.com/in/iffatul-anon/)

---