import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), 'knowledge')
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index(os.path.join(KNOWLEDGE_DIR, 'kb.index'))
with open(os.path.join(KNOWLEDGE_DIR, 'kb.pkl'), 'rb') as f:
    kb = pickle.load(f)
    texts = kb['texts']
    files = kb['files']

def search(query, k=3):
    q_vec = model.encode([query])
    D, I = index.search(q_vec, k)
    return [texts[i] for i in I[0]]
