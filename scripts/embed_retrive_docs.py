import os
import pandas as pd
import lancedb
from sentence_transformers import SentenceTransformer

# Initialize embedding model and LanceDB
embedder = SentenceTransformer("all-MiniLM-L6-v2")
db_dir = "data/lancedb"
table_name = "api_docs"

if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db = lancedb.connect(db_dir)

def embed_and_save_to_vectordb(chunks: list[str]):
    vectors = embedder.encode(chunks).tolist()
    data = [{
        "chunk_id": f"chunk_{i}", 
        "text": chunk, 
        "vector": vectors[i]
    } for i, chunk in enumerate(chunks)]
    df = pd.DataFrame(data)
    table = db.create_table(table_name, data=df, mode="overwrite")
    return table

def search_vectordb(query: str, top_k: int = 5):
    if table_name not in db.table_names():
        return []
    table = db.open_table(table_name)
    query_vec = embedder.encode([query])[0]
    results = table.search(query_vec).limit(top_k).to_df()
    return results["text"].tolist()
