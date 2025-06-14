import faiss
import pickle
from sentence_transformers import SentenceTransformer
from app.config import INDEX_PATH, CHUNKS_PATH

model = SentenceTransformer("all-MiniLM-L6-v2")

with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)

index = faiss.read_index(INDEX_PATH)

def get_top_k_chunks(question, k=5):
    question_embedding = model.encode([question])
    distances, indices = index.search(question_embedding, k)
    return [chunks[i] for i in indices[0]]
