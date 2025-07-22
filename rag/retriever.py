def search(query, k=5):
    q_vec = model.encode([query])
    _, I = index.search(q_vec, k)
    return df.iloc[I[0]]
