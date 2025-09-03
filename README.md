## RAG_Qdrant — RAG tabanlı Soru-Cevap Sistemi (Qdrant + Sentence-Transformers + Ollama + Streamlit)

Bu proje; web sayfalarını indirip temizleyen, metni parçalara ayırıp gömme (embedding) oluşturan ve Qdrant vektör veritabanına yükleyen; sonrasında da Ollama ile LLM çağırarak RAG (Retrieval-Augmented Generation) yanıtları üreten uçtan uca bir örnektir. Ayrıca iki farklı Streamlit arayüzü içerir: tam sayfa uygulama ve sayfaya gömülebilen açılır sohbet penceresi.


### Özellikler
- Web sayfalarından içerik toplama ve temizleme (trafilatura)
- Kelime bazlı metin parçalama (chunking)
- Sentence-Transformers ile gömme üretimi (BAAI/bge-m3)
- Qdrant koleksiyonuna upsert ve filtreli arama (kategori desteği)
- Ollama üzerinden Gemma modelini çağırarak RAG yanıtı üretme
- Streamlit tabanlı iki UI: `ui/app.py` (tam sayfa) ve `ui/chatbot/app.py` (yüzen sohbet)


### Mimari Genel Bakış
- `src/ingestion`: Veri alma ve hazırlama
  - `fetcher.py`: URL'den temiz metin indirir (trafilatura)
  - `chunker.py`: Metni kelime bazlı parçalara böler
  - `loader.py`: (boş dosya — gelecekte genişletmeye açık)
- `src/embeddings/embedder.py`: Sentence-Transformers ile embedding üretir (BAAI/bge-m3, 1024 boyut)
- `src/rag/retriever.py`: Qdrant'tan en alakalı parçalara (chunk) vektör benzerliğiyle erişir; isteğe bağlı kategori filtresi uygular
- `src/rag/llm_runner.py`: Ollama aracılığıyla Gemma modelini çağırır
- `src/rag/rag_chain.py`: RAG zinciri; sorguyu embed eder, bağlamı getirir, prompt'u oluşturur ve LLM cevabını döndürür
- `scripts/`: Uçtan uca iş akışını başlatan yardımcı betikler
  - `run_ingest.py`: JSON listedeki URL'leri indirir, chunk'lar, embed eder ve Qdrant'a yükler
  - `add_indexes.py`: Qdrant'ta `category` ve `subcategory` alanları için payload index oluşturur
  - `run_query.py`: Komut satırından RAG sorgusu çalıştırır (opsiyonel kategori filtresi alır)
- `ui/`: Streamlit arayüzleri ve stiller


### Gereksinimler
- Python 3.10+ (önerilir)
- Qdrant (Cloud veya Docker ile lokal)
- Ollama (lokalde LLM çalıştırmak için)


### Kurulum
1) Sanal ortam ve bağımlılıklar

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

# Projede kullanılan ancak requirements.txt içinde yer almayan paketler:
pip install tqdm pydantic-settings ollama
```

2) Qdrant
- Qdrant Cloud hesabı oluşturabilir veya Docker ile lokalde başlatabilirsiniz:
```powershell
docker run -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

3) Ollama ve model kurulumu
- Ollama yükleyin ve modeli indirin:
```powershell
# Ollama yükleme: https://ollama.com (kurulum sihirbazını izleyin)
ollama pull gemma3:4b
```

4) Ortam değişkenleri (.env)
Proje köküne `.env` dosyası oluşturun:
```dotenv
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY= # Lokal için boş bırakılabilir; Cloud kullanıyorsanız anahtarınızı girin
COLLECTION_NAME=my_rag_data
EMBEDDING_MODEL_NAME=BAAI/bge-m3
```


### Veri Formatı
`data/urls.json` dosyasında her satır bir sayfayı temsil eder:
```json
{
  "url": "https://www.ornek.com/sayfa",
  "category": "KategoriAdı",
  "subcategory": "AltKategoriAdı"
}
```
Örnek dosya proje içinde mevcuttur ve Etiya sitelerinden alınmış örnek URL'ler içerir.


### İndeksleme / Ingestion
Koleksiyon ilk ingestion sırasında oluşturulur ve `TEXT` ağırlıklı payload şeması atanır. Gömme boyutu `1024` olarak ayarlanır (BAAI/bge-m3 uyumludur).

```powershell
python scripts/run_ingest.py
```

İsteğe bağlı: `category` ve `subcategory` alanları için payload index oluşturmak isterseniz:
```powershell
python scripts/add_indexes.py
```


### Komut Satırından Sorgu (RAG)
```powershell
python scripts/run_query.py
# Çalıştırınca soru ve (opsiyonel) kategori filtresi girmenizi ister
```


### Streamlit Arayüzleri
Tam sayfa uygulama:
```powershell
streamlit run ui/app.py
```

Yüzen sohbet penceresi (gömülebilir mini arayüz):
```powershell
streamlit run ui/chatbot/app.py
```


### Önemli Parametreler ve Varsayılanlar
- Embedding modeli: `BAAI/bge-m3` (değiştirmek için `.env` → `EMBEDDING_MODEL_NAME`)
- Gömme boyutu: `1024` (Qdrant koleksiyonu bu boyutla oluşturulur)
- RAG sonuç sayısı: `top_k` (UI'da slider; `scripts/run_query.py` içinde `get_rag_response(..., top_k=7)` varsayılan)
- LLM (Ollama): `gemma3:4b` (`src/rag/llm_runner.py` içinde)
- Chunking: `split_text(text, max_words=300, overlap=50)` kelime bazlı


### Dosya Yapısı
```text
data/
  raw/                    # (boş)
  processed/              # (boş)
  urls.json               # İndirilip işlenecek URL listesi
scripts/
  run_ingest.py           # İndirme → chunk → embed → Qdrant upsert
  run_query.py            # CLI üzerinden RAG sorgusu
  add_indexes.py          # Qdrant payload index (category/subcategory)
src/
  config/settings.py      # Pydantic Settings (.env)
  embeddings/embedder.py  # Sentence-Transformers ile gömme
  ingestion/fetcher.py    # Trafiliatura ile sayfa metni
  ingestion/chunker.py    # Kelime bazlı chunking
  ingestion/loader.py     # (boş — gelecekte kullanım için)
  rag/retriever.py        # Qdrant arama + opsiyonel kategori filtresi
  rag/llm_runner.py       # Ollama (Gemma 3 4B) ile sohbet
  rag/rag_chain.py        # RAG akışı ve şablon
ui/
  app.py                  # Tam sayfa Streamlit uygulaması
  chatbot/app.py          # Yüzen chat penceresi arayüzü
  style.css               # Genel stil
  chatbot/style.css       # Sohbet stil dosyası
```


### Nasıl Çalışır? (Uçtan Uca)
1) `scripts/run_ingest.py`
   - `data/urls.json` → sayfa metni indir ve temizle (`trafilatura`)
   - Metni chunk'lara ayır (`chunker.py`)
   - Her chunk için embedding üret (`embedder.py`)
   - Qdrant koleksiyonunu yoksa oluştur, noktaları upsert et (payload: text, source_url, category, subcategory)

2) `src/rag/rag_chain.py`
   - Kullanıcı sorusunu embed eder
   - Qdrant'tan en yakın chunk'ları getirir (`retriever.py`)
   - RAG prompt'unu oluşturur ve Ollama'ya gönderir (`llm_runner.py`)
   - Türkçe yanıt döner

3) `ui/app.py` veya `ui/chatbot/app.py`
   - Kullanıcı etkileşimini yönetir, RAG zincirini çağırır, bağlamı gösterir


### Sorun Giderme
- Bağımlılıklar: `tqdm`, `pydantic-settings`, `ollama` paketleri `requirements.txt` içinde bulunmuyor olabilir. Yüklediğinizden emin olun:
  ```powershell
  pip install tqdm pydantic-settings ollama
  ```
- Qdrant bağlantısı: `QDRANT_URL` ve `QDRANT_API_KEY` değerlerini `.env` içinde doğru ayarlayın. Lokal kullanımda `QDRANT_API_KEY` boş olabilir.
- Ollama model bulunamadı: `ollama pull gemma3:4b` komutunu çalıştırın ve Ollama servisi çalışıyor olsun.
- Trafiliatura çıkarımı `None` dönüyor: Bazı sayfalar için içerik çıkarımı başarısız olabilir; bu durumda URL atlanır (loglarda görebilirsiniz).


### Güvenlik ve Notlar
- İnternetten içerik indirirken lisans ve telif haklarına dikkat edin.
- Qdrant Cloud kullanıyorsanız API anahtarınızı gizli tutun; `.env` dosyasını VCS dışında saklayın.


### Lisans
Bu depo için lisans bilgisi belirlenmemiştir. Kullanım koşullarını projenizin ihtiyaçlarına göre ekleyiniz.


