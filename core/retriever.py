import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FOLDER = os.path.join(BASE_DIR, "../index")
VECTOR_INDEX_PATH = os.path.join(INDEX_FOLDER, "vector.index")
CHUNK_STORE_PATH = os.path.join(INDEX_FOLDER, "chunks.pkl")
MODEL_NAME = "all-MiniLM-L6-v2"


def load_index():

    if not os.path.exists(VECTOR_INDEX_PATH):
        from core.ingest import run_ingest
        print("FAISS index not found. Rebuilding index from source files...")
        run_ingest()

    return faiss.read_index(VECTOR_INDEX_PATH)


def load_chunks():

    with open(CHUNK_STORE_PATH, "rb") as f:

        return pickle.load(f)
    

def get_relevant_chunks(query, top_k = 3):

    print(f"Searching for: {query}")
    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode([query])

    index = load_index()
    chunks = load_chunks()

    print("Performing similarity search")
    distances, indices = index.search(query_embedding, top_k)

    res = []
    
    for i in indices[0]:
        res.append(chunks[i])  
    
    return res