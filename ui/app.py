import sys, os
from pathlib import Path
import streamlit as st

# --- kök dizini Python path’e ekle (IDE + streamlit run için) ---
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ----- internal imports -----
from src.rag.rag_chain import get_rag_response
from src.rag.retriever import get_top_chunks
from src.embeddings.embedder import get_embedding
from src.config.settings import get_settings
from ui.components.sidebar import sidebar

# ---------- page config ----------
st.set_page_config(page_title="Etiya Bilgi Asistanı", layout="wide")
css = Path(__file__).with_name("style.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


st.title("💬 Etiya Bilgi Asistanı")

# ------------- giriş -------------
query = st.text_input(
    "📝 Soru Yazın",
    placeholder="Örnek: CRM çözümünün temel özellikleri nelerdir?"
)

# ------------- sidebar -----------
category_filter, top_k = sidebar(
    ["Tümü", "Hakkımızda", "Ürünler", "Çözümler", "Servisler", "EngageHub", "İletişim"]
)

# ------------- buton & sonuç -----
if st.button("🚀 Cevapla", key="ask_btn") and query:
    with st.spinner("Yanıt üretiliyor…"):
        answer = get_rag_response(query, category_filter=category_filter, top_k=top_k)

    st.markdown("### 📄 Yanıt")
    st.write(answer)

    # Bağlamı göster
    with st.expander("🔎 Kullanılan Bağlam"):
        ctxs = get_top_chunks(get_embedding(query), category=category_filter, top_k=top_k)
        for i, c in enumerate(ctxs, 1):
            st.markdown(f"**[{i}]** {c}")

# --------- footer ------------
settings = get_settings()
st.markdown(
    f"""
    <div class="footer">
      Model <strong>gemma3:4b</strong> · Embedding <strong>{settings.embedding_model_name}</strong> ·
      Koleksiyon <strong>{settings.collection_name}</strong>
    </div>
    """,
    unsafe_allow_html=True,
)
