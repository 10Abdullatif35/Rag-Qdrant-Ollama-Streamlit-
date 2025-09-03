# src/ingestion/chunker.py

def split_text(text: str, max_words: int = 300, overlap: int = 50) -> list[str]:
    """
    Uzun bir metni kelime bazlı chunk'lara ayırır.

    Args:
        text (str): Parçalanacak metin
        max_words (int): Her chunk'taki maksimum kelime sayısı
        overlap (int): Chunk'lar arası kelime örtüşmesi

    Returns:
        list[str]: Parçalanmış metin blokları
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words - overlap):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks
