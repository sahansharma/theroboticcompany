import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss

df = pd.read_csv("data/products.csv")
model = SentenceTransformer('all-MiniLM-L6-v2')
texts = df["ProductName"] + " " + df["Category"] + " " + df["Brand"]
vectors = model.encode(texts.tolist())

# Save to FAISS
index = faiss.IndexFlatL2(384)
index.add(vectors)
