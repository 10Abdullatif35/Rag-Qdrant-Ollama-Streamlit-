# scripts/run_ingest.py

import json
import uuid
from pathlib import Path
from tqdm import tqdm

from src.config.settings import get_settings
from src.ingestion.fetcher import fetch_clean_text
from src.ingestion.chunker import split_text
from src.embeddings.embedder import get_embedding
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# Ayarları .env üzerinden al
settings = get_settings()

# Qdrant istemcisi
client = QdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key
)

from qdrant_client.models import VectorParams, Distance, PayloadSchemaType

# Koleksiyon oluştur
if not client.collection_exists(settings.collection_name):
    client.create_collection(
        collection_name=settings.collection_name,
        vectors_config=VectorParams(
            size=1024,
            distance=Distance.COSINE
        )
    )

    # Ardından payload schema’yı ayarla
    client.set_payload_schema(
        collection_name=settings.collection_name,
        schema={
            "category": PayloadSchemaType.KEYWORD,
            "subcategory": PayloadSchemaType.KEYWORD,
            "source_url": PayloadSchemaType.KEYWORD,
            "text": PayloadSchemaType.TEXT
        }
    )


# JSON yolunu tanımla
URLS_PATH = Path("data/urls.json")

# Veriyi oku
with open(URLS_PATH, "r", encoding="utf-8") as f:
    url_list = json.load(f)

points = []

print(f"🔍 {len(url_list)} URL işleniyor...\n")

# Her URL için işle
for item in tqdm(url_list, desc="📄 Sayfa işleniyor"):
    url = item["url"]
    category = item.get("category", "Bilinmiyor")
    subcategory = item.get("subcategory", "Genel")

    text = fetch_clean_text(url)
    if not text:
        print(f"❌ Veri alınamadı: {url}")
        continue

    chunks = split_text(text)

    for chunk in chunks:
        vector = get_embedding(chunk)
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": chunk,
                "source_url": url,
                "category": category,
                "subcategory": subcategory
            }
        )
        points.append(point)

# Tüm vektörleri Qdrant'a yükle
client.upsert(
    collection_name=settings.collection_name,
    points=points
)

print(f"\n✅ {len(points)} adet veri Qdrant'a başarıyla yüklendi.")
