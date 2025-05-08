import os
import pickle
from sentence_transformers import SentenceTransformer
import faiss

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # the base dir where the file is at
DOCS_FOLDER = os.path.join(BASE_DIR, "../data" ) # the dir to store the txt file 
INDEX_FOLDER = os.path.join(BASE_DIR, "../index")  # dir to store the vector index and chunk files
VECTOR_INDEX_PATH = os.path.join(INDEX_FOLDER, "vector.index")  # path to save/load the FAISS vector index
CHUNK_STORE_PATH = os.path.join(INDEX_FOLDER, "chunks.pkl")     # path to save/load text chunks 
CHUNK_SIZE = 50                                                 
MODEL_NAME = "all-MiniLM-L6-v2"                                 


def read_documents(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r") as f:
                documents.append(f.read())
    return documents


def chunk_text(text, chunk_size):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


def build_vector_store(chunks):
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Embedding chunks...")
    embeddings = model.encode(chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print(f"Embedded and indexed {len(chunks)} chunks.")
    return index


def save_vector_index(index):
    faiss.write_index(index, VECTOR_INDEX_PATH)
    print(f"Saved FAISS index at {VECTOR_INDEX_PATH}")


def save_chunks(chunks):
    with open(CHUNK_STORE_PATH, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Saved chunk metadata at {CHUNK_STORE_PATH}")


def ingest_pipeline():
    print("Starting ingestion process...")

    os.makedirs(INDEX_FOLDER, exist_ok=True)

    docs = read_documents(DOCS_FOLDER)
    print(f"Read {len(docs)} documents.")

    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc, CHUNK_SIZE))

    print(f"Total chunks created: {len(all_chunks)}")

    index = build_vector_store(all_chunks)
    save_vector_index(index)
    save_chunks(all_chunks)

    print("Ingestion pipeline completed successfully.")