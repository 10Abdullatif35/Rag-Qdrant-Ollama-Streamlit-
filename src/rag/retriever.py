# src/rag/retriever.py

from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from src.config.settings import get_settings

# Ayarları al
settings = get_settings()

# Qdrant istemcisi oluştur
client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key
)

def get_top_chunks(
    query_vector: List[float],
    category: Optional[str] = None,
    top_k: int = 7
) -> List[str]:
    """
    Qdrant'tan en yakın chunk'ları getirir.

    Args:
        query_vector (List[float]): Sorgunun embedding vektörü
        category (Optional[str]): Filtre olarak kategori (isteğe bağlı)
        top_k (int): Kaç adet sonuç getirilsin

    Returns:
        List[str]: Chunk metinleri
    """
    # Filtre oluştur (kategori varsa)
    qdrant_filter = None
    if category:
        qdrant_filter = Filter(
            must=[
                FieldCondition(
                    key="category",
                    match=MatchValue(value=category)
                )
            ]
        )

    results = client.search(
        collection_name=settings.collection_name,
        query_vector=query_vector,
        limit=top_k,
        query_filter=qdrant_filter
    )

    return [hit.payload["text"] for hit in results]
