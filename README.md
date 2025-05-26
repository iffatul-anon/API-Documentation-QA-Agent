# API-Documentation-QA-Agent
This Al agent can answer natural language questions about a specific API, using its official documentation as the knowledge base. The agent use vector database embeddings to retrieve relevant context from the documentation before generating an answer with a Large Language Model (LLM).

## 🚀 Features
* 📚 Ingests API documentation (Markdown, text, or HTML)
* ✂️ Chunks and embeds documentation using a semantic model
* 🧠 Stores embeddings in a vector database for semantic search
* 🔍 Retrieves relevant context based on user queries
* 💬 Answers user questions using a Retrieval-Augmented Generation (RAG) pattern
* 🧾 Interface Streamlit
* ✅ Answers grounded in real documentation (no hallucinations)
* Basic conversation history to handle follow-up questions. 

## 🧱 Tech Stack
| Component           | Choice                                      |
|---------------------|---------------------------------------------|
| Language            | Python                                      |
| LLM                 | Groq API ( llama-3.3-70b-versatile )        |
| Agent Framwork      | Phidata                                     |
| Vector DB           | LanceDB                                     |
| Embedding           | Sentence Transformers ( all-MiniLM-L6-v2 )  |
| Chunking            | LangChain Text Splitters                    |
| Scraping            | Unstructured Library                        |
| Coversation History | JSON                                        |
| Interface           | Streamlit                                   |


## 📋 System Requirements

* Python 3.8 or higher
* 2GB free disk space (for vector database storage)
* Active internet connection (for LLM API access)
* Groq API account and key

## 🔧 Dependencies

Core dependencies:
* `streamlit`: Web interface
* `phi-agent`: LLM agent framework
* `sentence-transformers`: Document embedding
* `lancedb`: Vector database
* `langchain`: Text chunking
* `unstructured`: Document parsing
* `python-dotenv`: Environment management

See `requirements.txt` for complete list of dependencies.

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


## 📁 Project Structure
```bash
api-docs-qa-agent/
│
├── data/                    # VectorDB files, Conversation history
├── scripts/                 # Scripts for ingestion, embedding, retrieval
│   ├── chunk_docs.py
│   ├── conversation_load_and_save.py
│   ├── embed_retrive_docs.py
│   ├── load_docs.py
│   └── query_agent.py
├── main.py                  # interface to interact with the agent
├── requirements.txt
└── README.md
```

## 🛠️ Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/iffatul-anon/API-Documentation-QA-Agent
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

4. **Run the application**
```bash
streamlit run main.py
```

## 💡 Usage Examples

1. **Loading Documentation**
```
1. Open the application in your browser
2. In the sidebar, enter the URL of the API documentation
3. Click "Load Docs" to process the documentation
4. Wait for confirmation that chunks are saved to VectorDB
```

2. **Basic API Questions**
```
You can ask questions like:
Q: "What are the main features of this API?"
Q: "How do I authenticate with the API?"
Q: "Show me example code for making a GET request"
Q: "What are the available endpoints?"
Q: "What parameters does the /users endpoint accept?"
```

3. **Follow-up Questions**
```
The agent maintains conversation context for follow-ups:
Q: "How do I create a new user?"
Q: "What parameters are required?"
Q: "Can you show me an example request?"
```

4. **Documentation Management**
```
- Clear chat history using the "Clear Chat History" button in sidebar
- Load multiple API docs by entering different URLs
- Each new document load adds to the knowledge base
```

## 🚫 Limitations

1. **Documentation Format**
   - Works best with well-structured HTML documentation
   - May have reduced performance with PDF files
   - Some dynamic content may not be properly scraped

2. **Query Context**
   - Limited conversation history (last 5 messages)
   - Best for focused, specific questions
   - Complex multi-step workflows may need to be broken down

3. **Response Time**
   - Initial document loading may take time depending on size
   - Response generation typically takes 2-5 seconds
   - Network delays may affect LLM response time

## 🔍 Troubleshooting

1. **Application Won't Start**
   - Verify Python version: `python --version`
   - Ensure virtual environment is activated
   - Check all dependencies are installed: `pip freeze`
   - Verify GROQ_API_KEY in .env file

2. **Document Loading Fails**
   - Check URL is accessible in browser
   - Verify internet connection
   - Try with a different documentation URL
   - Check console for specific error messages

3. **No Response from Agent**
   - Verify GROQ_API_KEY is valid
   - Check internet connection
   - Ensure documentation was properly loaded
   - Try clearing chat history and reloading docs

4. **Poor Quality Responses**
   - Try rephrasing the question
   - Ensure relevant documentation is loaded
   - Check if question is within loaded doc scope
   - Consider loading additional related documentation

## 📞 Support

For issues, questions, or contributions:
1. Open an issue on GitHub
2. Provide detailed error messages if applicable
3. Include steps to reproduce any problems
4. Specify your system configuration

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
