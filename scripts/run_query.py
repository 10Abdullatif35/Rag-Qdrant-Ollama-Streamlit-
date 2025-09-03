# scripts/run_query.py

from src.rag.rag_chain import get_rag_response

if __name__ == "__main__":
    question = input("❓ Soru: ").strip()

    if not question:
        print("Lütfen bir soru girin.")
        exit()

    category = input("🎯 (Opsiyonel) Kategori filtresi [boş bırak = tümü]: ").strip() or None

    print("\n🔎 Cevap aranıyor...\n")

    response = get_rag_response(question, category_filter=category)

    print("📄 Yanıt:")
    print(response)
