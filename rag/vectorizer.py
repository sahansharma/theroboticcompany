import os
import glob
import pickle
from sentence_transformers import SentenceTransformer
import faiss

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), 'knowledge')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Gather all text from knowledge base
texts = []
file_map = []
for filepath in glob.glob(os.path.join(KNOWLEDGE_DIR, '*.md')) + glob.glob(os.path.join(KNOWLEDGE_DIR, '*.txt')):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
        texts.append(content)
        file_map.append(filepath)

vectors = model.encode(texts)
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# Save index and mapping
faiss.write_index(index, os.path.join(KNOWLEDGE_DIR, 'kb.index'))
with open(os.path.join(KNOWLEDGE_DIR, 'kb.pkl'), 'wb') as f:
    pickle.dump({'texts': texts, 'files': file_map}, f)
