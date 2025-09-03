# src/ingestion/fetcher.py

import trafilatura

def fetch_clean_text(url: str) -> str | None:
    """
    Verilen bir URL'den temizlenmiş metni çeker.

    Args:
        url (str): Web sayfası adresi

    Returns:
        str | None: Temiz metin veya None (başarısızsa)
    """
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return trafilatura.extract(downloaded)
    return None
