# src/embeddings/embedder.py
from src.config.settings import get_settings
from sentence_transformers import SentenceTransformer

settings = get_settings()
_model = SentenceTransformer(settings.embedding_model_name)

def get_embedding(text: str) -> list[float]:
    """
    Verilen metni embedding (vektör) haline getirir.

    Args:
        text (str): Chunk metni

    Returns:
        list[float]: Embedding vektörü
    """
    prompt = f"passage: {text}"  # BGE-m3 için prompt zorunludur
    return _model.encode(prompt).tolist()
