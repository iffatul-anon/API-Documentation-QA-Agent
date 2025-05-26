"""
This module handles document embedding and vector similarity search functionality.

It uses the sentence-transformers library to create embeddings and LanceDB
for efficient vector storage and similarity search. The module supports both
storing new document embeddings and searching for similar documents using
semantic similarity.

Dependencies:
    - sentence-transformers
    - lancedb
    - pandas
"""

import os
import pandas as pd
import lancedb
from sentence_transformers import SentenceTransformer
from typing import List, Optional, Any
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize embedding model and LanceDB
embedder = SentenceTransformer("all-MiniLM-L6-v2")
db_dir = "data/lancedb"
table_name = "api_docs"

if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db = lancedb.connect(db_dir)

def embed_and_save_to_vectordb(chunks: List[str]) -> Any:
    """
    Convert text chunks to embeddings and save them in the vector database.

    This function processes a list of text chunks, generates their vector
    embeddings using the sentence-transformers model, and stores them in
    LanceDB for later similarity search.

    Args:
        chunks (List[str]): List of text segments to be embedded. Each chunk
            should be a meaningful piece of text, typically 500-1000 characters.

    Returns:
        Any: LanceDB table object containing the stored embeddings.

    Example:
        >>> chunks = ["First document", "Second document"]
        >>> table = embed_and_save_to_vectordb(chunks)
        >>> print(f"Saved {len(chunks)} documents to vector store")
    """
    vectors = embedder.encode(chunks).tolist()
    data = [{
        "chunk_id": f"chunk_{i}", 
        "text": chunk, 
        "vector": vectors[i]
    } for i, chunk in enumerate(chunks)]
    df = pd.DataFrame(data)
    table = db.create_table(table_name, data=df, mode="overwrite")
    return table

def search_vectordb(query: str, top_k: int = 5) -> List[str]:
    """
    Search for similar documents in the vector database.

    This function takes a query string, converts it to a vector embedding,
    and performs a similarity search in the vector database to find the
    most relevant document chunks.

    Args:
        query (str): The search query string.
        top_k (int, optional): Number of most similar documents to return.
            Defaults to 5.

    Returns:
        List[str]: A list of the top_k most similar document chunks,
            ordered by similarity (most similar first).

    Example:
        >>> results = search_vectordb("How to authenticate?", top_k=3)
        >>> for doc in results:
        ...     print(f"Relevant doc: {doc[:100]}...")  # Print first 100 chars
    """
    if table_name not in db.table_names():
        return []
    table = db.open_table(table_name)
    query_vec = embedder.encode([query])[0]
    results = table.search(query_vec).limit(top_k).to_df()
    return results["text"].tolist()
