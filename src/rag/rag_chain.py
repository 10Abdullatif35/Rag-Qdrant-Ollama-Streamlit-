# src/rag/rag_chain.py
from typing import Optional
from src.embeddings.embedder import get_embedding
from src.rag.retriever import get_top_chunks
from src.rag.llm_runner import call_ollama

RAG_TEMPLATE = """
Aşağıda bazı doküman parçaları (context) verilmiştir. 
Soruya yalnızca bu bilgilere dayanarak, Türkçe cevap ver.

Context:
{context}

Soru: {question}
Cevap:
"""

def get_rag_response(question: str, category_filter: Optional[str] = None, top_k: int = 7) -> str:
    # 1) Sorguyu embed et
    q_vec = get_embedding(question)

    # 2) İlgili chunk’ları getir
    chunks = get_top_chunks(q_vec, category=category_filter, top_k=top_k)
    context = "\n\n---\n\n".join(chunks)

    # 3) Prompt oluştur
    prompt = RAG_TEMPLATE.format(context=context, question=question)

    # 4) LLM’e gönder
    answer = call_ollama(prompt)
    return answer
