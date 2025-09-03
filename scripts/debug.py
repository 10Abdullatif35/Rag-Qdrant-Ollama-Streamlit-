from src.embeddings.embedder import get_embedding
from src.rag.retriever import get_top_chunks

query = "müşteri ilişkileri ile ilgili çözümler"
embedding = get_embedding(query)

chunks = get_top_chunks(embedding, category="Ürünler")
for i, c in enumerate(chunks):
    print(f"\n[{i+1}] {c[:300]}...")
