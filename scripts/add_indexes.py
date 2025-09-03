# scripts/add_indexes.py
"""
Var olan koleksiyona category ve subcategory için payload index ekler.
Bir kez çalıştırmak yeterlidir.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType
from src.config.settings import get_settings

def main() -> None:
    settings = get_settings()

    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key
    )

    coll = settings.collection_name
    print(f"🔧 Koleksiyon: {coll}")

    # ---- category index ----
    try:
        client.create_payload_index(
            collection_name=coll,
            field_name="category",
            field_schema=PayloadSchemaType.KEYWORD,
        )
        print("✅ 'category' alanı için index oluşturuldu.")
    except Exception as e:
        print(f"ℹ️ 'category' index oluşturulamadı (belki zaten var): {e}")

    # ---- subcategory index ----
    try:
        client.create_payload_index(
            collection_name=coll,
            field_name="subcategory",
            field_schema=PayloadSchemaType.KEYWORD,
        )
        print("✅ 'subcategory' alanı için index oluşturuldu.")
    except Exception as e:
        print(f"ℹ️ 'subcategory' index oluşturulamadı (belki zaten var): {e}")

if __name__ == "__main__":
    main()
